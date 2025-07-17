# -*- coding: utf-8 -*-
"""
Easygame 6.0

:authors: Dickon Reed, <dickon@cantab.net>, Adam Rowell, <arowell@cantab.net>

So what is it?
==============

easygame is a Python library designed to make it as easy as possible
to write 2D graphics intensive programs such as games. It is based on
pygame by Pete Shinners, which in turned is based on SDL and
Python. So, it works on Windows, Linux and maybe MacOSX as well.

Easygame is a layer on top of pygame, and only redefines certain parts
of the pygame API. In fact all the pygame API is still available to
the user, and easygame only helps with animated 2D graphics, keyboard
input and timing. But, the easygame API is also complete enough that
simple programs won't need to access pygame directly at all, so you
can just focus on easygame to begin with and completely ignore the
fact that it is using pygame.

The easygame library itself is just a single python source file, and so should be placed on your PYTHONPATH if you already have a python installation.

From scratch, the easiest way on Windows to install easygame is to:

1. Install Python (I use python 3.1) available at:

   http://www.python.org/ftp/python/3.1.4/python-3.1.4.msi
   
2. Install pygame (I use pygame 1.5, but later versions should work)
   available at:
   
   http://pygame.org/ftp/pygame-1.9.1.win32-py3.1.msi
      
3. Copy easygame.py into your Python directory (eg Python31 in your
   Program Files directory)

Tutorial
========

Open a Python shell. You should see something like::

    Python 3.1 (r31:73574, Jun 26 2009, 20:21:35) [MSC v.1500 32 bit (Intel)] on win32
    Type "copyright", "credits" or "license" for more information.
    >>> 

Then type::

    from easygame import *

and press return. You should see a new black window appear labelled
``pygame window``. Somewhere on screen your Python shell window should
still be around, and should look a bit like this:

    Python 3.1 (r31:73574, Jun 26 2009, 20:21:35) [MSC v.1500 32 bit (Intel)] on win32
    Type "copyright", "credits" or "license" for more information.
    >>> from easygame import *
    >>> 

Congratulations! Everything is installed correctly. But the black
window is a little dull. Try typing some of the following in. Try to
guess what each one will do before you press return::

    line( (0,0), (600,100) )
    circle( (320,200), 40)
    printat( (100,100), 'Hello world')
    polygon ( [(200,300), (400,300), (300,400)])
    ellipse( ((100,100), (400,50)))
    lines( [(100,100), (150,50), (200,100), (250,50)])
    clearscreen()
    setmode( (200,100) )
    rectangle (((0,0), (199,99)), col=(255,255,255) )
    line ( (0,50), (199,50), width=10, col=(255,0,0))
    line ( (100,0), (100,99), width=10, col=(255,0,0) )

That's enough to do quite a lot of drawing work. You can even do
animation by putting a loop around the drawing commands.

Using setbatching() and tick()
-----------------------------

Normally, whenever you draw anything, it stays on the screen until you
draw over it. So you are likely to find that your animation will look
a bit flickery. Easygame has some tricks to help make animated
graphics look better. Try typing the following commands into a python
shell::

    setmode( (200,100) )
    setbatching(1)
    rectangle (((0,0), (199,99)), col=(255,255,255) )
    line ( (0,50), (199,50), width=10, col=(255,0,0))
    line ( (100,0), (100,99), width=10, col=(255,0,0) )

Unlike before, once the setbatching command has been executed nothing
will appear on the screen. But it is still being recorded inside the
computer. To make it appear, type::

    tick()

This means you get to control when the graphics appear on the
screen. So changes can appear all at once, rather than piece by
piece. Here's the rule:

*After setbatching(1), no graphics updates appear until the next
tick() command. This keeps happening until a setbatching(0) is
executed.*

Here's a simple example program. Put this into a text file, and then
use Python to run it. In idlefork you can open a file using the file
menu, and then use the Run program option under the run menu to make
it start. Can you guess what it will do before running it?::

    from easygame import *
    setbatching(1)
    size = 20
    while 1:
      clearscreen()
      circle( (320,200), radius=size, col=(255,0,0))
      size = size +1
      if size > 100: size = 20
      tick()

As an exercise, try predicting what commenting out any particular line
would do to the program.

What we've got so far is actually enough for a lot of animation, but
there's a problem. It is fiddly to get rid of things off the screen
without clearing the whole screen and redrawing everything. If you've
got an intricate pattern on screen, redrawing it every time you want
to change anything makes the computer work harder than it needs
to. Easygame has another trick to fix this; temporary drawing.

Using temporary drawing
-----------------------

The idea is to let some parts of the screen drawing be temporary, and
then get rid of just the temporary bits in order to do the animation.

Here's an example. It might be best to type each line in turn into a
python shell, so you can see it working step by step::

    from easygame import *
    circle((100, 100), radius=50, col=(255,0,0))
    circle( (150, 100), radius=50, col=(0,0,255), temp=1)
    circle( (125,150), radius=50, col=(0,255,0))

    cleartemp()

You should see a red circle appear. That's just a normal drawing
command. Then a blue circle appears, apparently as normal, followed by
a green circle. But the last line (the cleartemp() command) gets rid
of the blue circle. Note that you can still see the red circle
underneath; i.e. The blue circle hasn't just been relaced by a black
circle, but it has been removed, being replaced with the non-temporary
drawing (called the background) which was there before. Here's the
rule:

*Unless you set temp to true in the arguments of a drawing command,
the command will update the background. cleartemp() restores the
background.*

Here's an example program::

    from easygame import *
    h = getscreenheight()
    w = getscreenwidth()
    for y in range(h):
        line( (0,y), (w-1, y), col=(int(255.0*y/h), 0,0))

    x,y = w/2, h/2
    dx, dy = 1,1
    setbatching(1)

    while 1:
        circle( (x,y), 40, temp=1)
        if x > w-50 or x < 50: dx = -dx
        if y > h-50 or y < 50: dy = -dy
        x += dx
        y += dy
        tick()
        cleartemp()



This shows off a couple of new commands; getscreenwidth() and
getscreenheight() just tell you the current screen width and
height. The default is 640 and 480 respectively.

Controlling animation speed
===========================

Often you want to control the speed animations run at, rather than
just make them go as fast as the computer can. Look at this example
program::

    from easygame import *
    h = getscreenheight()
    w = getscreenwidth()
    x, y = w/2, h/2
    dx = 1
    setbatching(1)
    while 1:
        circle( (x,y), 40, temp=1)
        if x > w-50 or x < 50: dx = -dx
        tick(50)
        cleartemp()
        x += dx 

What's happening is that tick() automatically returns an estimate of
the time average time taken between calls to tick(). The example here
tries to make the ball move at 20 pixels per second. On a slow
computer, or a computer busy doing other things, the values returned
by tick() will be higher, so the ball moves more between each tick, so
the animation is jerkier but should still keep the right speed up.
Reading the keyboard

There are several commands for reading the keyboard. ispressed() finds
out if a particular key is pressed. waitforkey() waits until a key is
pressed, ignoring keys that are already down. getkey() is similar, but
doesn't wait for keys to be released first.

Here's some examples::

    if ispressed(K_LEFT): x = x -1
    ch = getkey() # find out a key that has been pressed
    waitforkey() # wait for a key to be pressed

How do you know which to use? Here's some advice:

* Use ispressed() when you are doing animation that shouldn't stop
  waiting for keys to be pressed.

* Use waitforkey() when you want to wait for the user to read a message
  before continuining

* Use getkey() if you want to know about each individual keypress,
  for example if the number of times that a key has been pressed matters.

Sometimes you need to say which key or keys you are interested in. You
describe a key by writing K then underscore in front of the name of
the key. The alphabetical keys are written in lower case. Here's the
complete list:

    K_0 K_1 K_2 K_3 K_4 K_5 K_6 K_7 K_8 K_9 K_AMPERSAND K_ASTERISK K_AT
    K_BACKQUOTE K_BACKSLASH K_BACKSPACE K_BREAK K_CAPSLOCK K_CARET K_CLEAR
    K_COLON K_COMMA K_DELETE K_DOLLAR K_DOWN K_END K_EQUALS K_ESCAPE
    K_EURO K_EXCLAIM K_F1 K_F10 K_F11 K_F12 K_F13 K_F14 K_F15 K_F2 K_F3
    K_F4 K_F5 K_F6 K_F7 K_F8 K_F9 K_FIRST K_GREATER K_HASH K_HELP K_HOME
    K_INSERT K_KP0 K_KP1 K_KP2 K_KP3 K_KP4 K_KP5 K_KP6 K_KP7 K_KP8 K_KP9
    K_KP_DIVIDE K_KP_ENTER K_KP_EQUALS K_KP_MINUS K_KP_MULTIPLY
    K_KP_PERIOD K_KP_PLUS K_LALT K_LAST K_LCTRL K_LEFT K_LEFTBRACKET
    K_LEFTPAREN K_LESS K_LMETA K_LSHIFT K_LSUPER K_MENU K_MINUS K_MODE
    K_NUMLOCK K_PAGEDOWN K_PAGEUP K_PAUSE K_PERIOD K_PLUS K_POWER K_PRINT
    K_QUESTION K_QUOTE K_QUOTEDBL K_RALT K_RCTRL K_RETURN K_RIGHT
    K_RIGHTBRACKET K_RIGHTPAREN K_RMETA K_RSHIFT K_RSUPER K_SCROLLOCK
    K_SEMICOLON K_SLASH K_SPACE K_SYSREQ K_TAB K_UNDERSCORE K_UNKNOWN K_UP
    K_a K_b K_c K_d K_e K_f K_g K_h K_i K_j K_k K_l K_m K_n K_o K_p K_q
    K_r K_s K_t K_u K_v K_w K_x K_y K_z 
    
More about printat and rectangles

``printat()`` normally uses the coordinates it is given as the middle of
the text. Sometimes you might want more control over the size of
text. For instance, you might want to underline the text, or place it
relative to something other than its center (or top left). There's a
couple of tricks in printat which help. Prinat, like the rest of the
easygame drawing commands, returns the rectangle that it covers. The
rectangle is returned as a special pygame data type, called a
Rect. You can see the full range of things you can do with Rect in the
pygame documentation, and I won't reproduce it here. They are really
useful; you can find the size of a rectangle, the location of the
edges; you can see if rectangles collide with things, and you can
change the size and move rectangles around.

Also, because the actual size of the text is difficult to work out,
you can have printat work out the size but not actually display the
text, by setting onlysize=1 in the arguments. Here's an example that
uses both facts about ``printat``::

    from easygame import *
    size = printat( (100,100), 'Hello world', topleft=1)
    line( (size.left,size.bottom+2), (size.right,size.bottom+2), width=2)
    border = size.inflate( 4,4)
    rectangle(border, width=2, col=(255,0,0))



    size2 = printat( (0,0), 'The Corner', onlysize=1)
    printat( (getscreenwidth()-size2.width, getscreenheight()-size2.height),
             'The Corner',topleft=1)
    getkey()

Here's some advice:

*Use printat with onlysize=1 to figure out how large text is.*

Advanced topics tutorial
------------------------
At this point you know enough to write fairly sophisticated programs
with easygame. Either read on through this tutorial for more advanced
techniques, or skip to the worked exercise below. There's a reference
at the end which you should use, but this refers to advanced topics
not covered up to this point. Just ignoring bits you don't understand
should be fine, though.



Timing
======

Sometimes you may want to pause your easygame based program for a
while without necessarily using the ``tick(fps)`` mechanism. Use the
``pause()`` command. For instance to wait for one second::

    pause(1000)

You may notice your computer running slowly even while easygame is in
the middle of a pause(). This is because to time the pause you ask for
accurately it is has to not do anything else, waiting for time to flow
by, ready to return the millisecond it should. If you don't mind if
the pause() takes a little bit longer than you ask for, you can add
rough=1 to the pause, like this:

    pause(10000,rough=1)

This means pause, for at least 10 seconds, but run other programs in
the mean time even if it means taking a fraction longer than 10
seconds. On a multiuser system, such as Linux with several users, you
should definetly use rough=1 as often as you can because it avoids
slowing down the computer for others.  Collison detection

Every drawing command returns a rectangle which is the bounding box of
the drawing. This means it is the smallest (non-rotated) rectangle
which encloses the entire drawing. These rectangles are represented as
pygame ``Rect`` objects. You can use these to do collision detection. For
instance::

    r1 = plotimage( (p1), 'player.tif')
    r2 = plotimage( (p2), 'bullet.gif')
    ...
    if r1.colliderect(r2):
       # bullet and player overlap
       ....
    if r1.collidepoint(p3):
       # p3 is inside r1
       ...

See invaders.py for a complete example of colliderect, and see the
pygame ``Rect`` documentation for more about the rectangle
operations. Note that this collision detection method doesn't do pixel
perfect collision; it is just checking if the rectangles
overlap. There are much more sophisticated ways of doing collision
detection, but this version of easygame doesn't support them.
Clipping

Easygame automatically clips all drawing to fit on the
screen. However, you can control the clipping to temporarily only
allow drawing on one part of the screen. For example, you may want to
have a control panel at one side of the screen, and the drawing on the
main "action" part of the screen not overwrite the control panel. You


can do this using the setclipping() command. For instance::

    setclipping( Rect( (10,10), (460,460) )
    # some drawing commands
    setclipping()

Note that ``setclipping()`` without any arguments resets the clipping to
cover the whole screen.. Similarly, using setmode() also sets the
clipping to cover the whole screen.

The Pos class
=============

You don't have to use the Pos ``class``, but quite often easygame
programs make heavy use of 2D positions and vectors. The ``Pos`` class
provides a data type that can hold 2D vectors (perhaps representing
positions), and provides methods to operate on them. Pos objects
(instances of the Pos class) also behave as sequences of length 2, so
can be used in all the places in easygame where coordinates are
required. Have a look at the Pos reference below for the full list of
operations possible with Pos objects, but here are some examples of
using Pos with easygame::

    line( getsize()/2, Pos(angle=30, magnitude=100)) # draw a line from
    # the center of the screen, out at 30 degress and length 100 pixels



    # move an object across the screen.
    pos = Pos (100,100)
    vel = Pos(angle=30)
    while 1:
       plotimage(pos, 'mypicture.jpg', temp=1)
       pos = pos + vel

You should be aware that ``Pos`` objects are immutable. This means that
once you have a Pos object, you can't change it's value. Operators
like += and ``p.setx()`` create new Pos objects; they don't have change
the object itself. So you can use Pos objects at hash table keys.

The Sprite System
=================

Again, you don't have to use this. Some people find that when they are
writing code to deal with large numbers of moving objects, the code
can get quite long winded. The easygame sprite system lets you have
easygame keep track of drawing, location and movement of a number of
*sprites*. Each sprite is represented by an instance of the ``Sprite``
class. The special ``spritetick()`` command arranges for all
registered sprites to have their position be updated, and be drawn
properly, as well as performing the ``cleartemp()`` and ``tick()``
operations that most easygame based animation programs will
use. Here's a simple example that has a circle move across the screen::

    from easygame import *
    sprobj = Sprite( Pos(100,100),  Pos(direction=30, magnitude=100), circle, 8, col=(255,0,0) )
    for i in xrange(500):
      spritetick(100)
    delsprite(sprobj)

The first line creates a ``Sprite`` object, which automatically
registers itself. The first argument to the ``Sprite`` constructor is
the initial position of the sprite. The second argument is the
direction vector of the ``Sprite`` (here using the ``Pos`` class
explained above). Next comes the name of the easygame command to draw
the sprite, followed by the options that command requires. Any Python
function which takes a position as a first argument and accepts the
temp argument is valid here, and this includes most of the easygame
commands. But you can also define your own procedure to be called to
draw the sprite. Or, you can subclass ``Sprite`` to implement a
constructor, and ``draw()`` and ``tick()`` methods yourself. See the
``Sprite`` reference information below for further details.

Note that pygame also has a sprite system, and the two are not related.

Multiple temporary layers
=========================

Until now we have shown simple temporary drawing. It is also possible
to have ``cleartemp()`` remove only some temporary drawing. The value
of the temp keyword argument supplied to operands can be any true
value (i.e. almost anything apart from ``[]``, ``''``, ``0`` and
``None``). ``cleartemp()`` takes an optional argument, and if given it
will only remove temporary drawing with a matching temp
value. Therefore, you can create different temporary layers by using
different true values for the temp argument. Here's an example::


    from easygame import *
    setbatching(1)
    printat( (0,0), 'BACKGROUND!', angle=30, pointsize=130, fg=(128,128,128),topleft=1)
    count = 0
    while 1:
        count+=1
        for t in range(4):
            temp =t+1
            for i in range(100):
                cleartemp(temp)
                printat( (i*4+100, temp*100), 'level',t+1,'run',count,temp=temp)
                tick(100)



A warning: what ``cleartemp()`` actually does is expose the background
for the bounding rectangles of the appropriate drawing operations. If
parts of temporary drawing on other areas overlaps temporary drawing
you remove using cleartemp(), then the overlapping parts of the
temporary drawing on other layers will also be overwritten by the
background. There's no concept of a stacking order of temporary
layers; what you draw goes on the screen in the order you draw it, and
cleartemp() is just another way of drawing.

``Manipulating surfaces``

It takes the system a little time to rotate and zoom on images and
text, and to render text. Also, you may want to do some drawing and
then replicate that drawing over differnet parts of the screen. For
this reason, you can use the ``Surface`` objects from pygame. The
``getat()`` command takes a rectangle and returns the contents of the
screen over that area as a rectangle. ``plotimage()``, ``printat()`` and
``superblit()`` can take onlygetsurface=1 as an argument and return the
``Surface`` they would have displayed. ``superblit()`` can display a surface
on the screen. The example tiler.py uses surfaces to read the contents
of a part of the screen and tile it across the screen, as well as to
save a piece of the screen to disk as a bitmap. invaders.py uses
surfaces to avoid having to do image zooming on every frame.  Use the
rest of pygame when you need to

That's about it as far as easygame is concerned. Easygame is built on
top of pygame, and pygame can do a lot more stuff. Much of this stuff
is so straightforwrad that there's no way easygame can make it any
easier. There's lots of good examples and documentation that come with
pygame. Here's an example of using easygame with some of the pygame
APIs::

    from easygame import *
    while 1:
      if ispressed(K_SPACE):
        pygame.image.save(getarea(), 'screendump.bmp')  

      if pygame.mouse.get_pressed()[0]:
        circle( pygame.mouse.get_pos(), 10) 

      tick(100)


A worked exercise- Pacman!
==========================

Let's go through stage by stage how to write a game with easygame. You
can find my version of each step in the easygame distribution
(e.g. pacman1a.py), but I suggest you might like to try writing it
yourself. 

A note for experienced programmers: I've tried to use a reasonably
simple subset of python here, and there's are obviously more
structured ways of writing this.

Phase 1: A moving pacman Pacman
-------------------------------

1a; just draw a simple pacman on the screen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You shouldn't need more than 5 lines of code. At this stage I just use
a solid circle to represent the pacman. You may find it handy to write
getkey() as the last line of your program, so you can see the program
output before it stops.

1b; make the pacman move, leaving a trail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We want the pacman to move about the screen. But to keep things
simple, for this stage lets just make the pacman move and worry about
removing the trail in the next step. You should end up with an
expanding line of pacman characters as the program runs. Don't worry
what happens when the pacman goes off the screen, we'll deal with that
later as well.

You'll probably need some variables to keep track of the position of
the pacman.

1c; getting rid of the trail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You could just get rid of the trail by clearing the screen each
time. But that's very inefficient; later we'll have the maze and stuff
on the screen, and we don't want to have to redraw that every time
pacman moves. Instead we'll use the temp=1/cleartemp() thing explained
above to make the pacman a temporary object, so that we can easily get
rid of the trail. Have a look through the *Using temporary drawin*
section above if you aren't sure how to do this.

1d; adding steering
~~~~~~~~~~~~~~~~~~~

We need the player to be able to control the direction pacman is
heading in. If you don't already have them, you might need some
variables to store which direction the pacman is heading in. Then you
can use ispressed() to look at which keys are down on the keyboard.

1e; dealing with the edges of the screen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to decide what happens when pacman reaches the edge of the
screen: does he keep going off the screen, bounce off, stop, or
wraparound to the other side? You may find getscreenheight() and
getscreenwidth() useful to find out how big the screen is, or you
could just assume it is 640 by 480 (as is this the default in this
version of easygame). But it's Good Karma to not assume this, mainly
because if you change the screen size later you don't have to through
your whole program updating it for the new screen size.  Pacman1f;
slowing it down

In real pacman games the pacman doesn't move as fast as in the
previous version, and can only change direction at maze corners. We
don't have a maze yet, but we can first experiment with having the
pacman change direction only sometimes. The easiest way to do this is
to make pacman jump a little each time. Later we'll change the program
to have smooth transitions between jumps.

The tick() command can be told to not allow more than a certain number
of ticks per second. You give the number as a paramter.

Phase 2; Pacman moving around a maze
------------------------------------

2a; drawing a maze
~~~~~~~~~~~~~~~~~~

We need a maze for the pacman to move around. To start with, just draw
the maze. You'll need walls, and while you're at it you might as well
as pills for pacman to eat. Later we'll make the maze a more
interesting shape, and have the pacman interact with the maze.
Pacman2b; adding a real maze

First we need a maze to move around. Later we'll need to find out what
shape is in the maze, so you need a datastructure where you can look
up what is at maze location. I suggest a dictionary mapping maze
coordinate 2-tuples to cell types. That's just a fancy way of saying
something like::

    maze = {}
    maze[ (0,0) ] = '#' 
    ...
    maze[ (1,1)] = '.'
    ...


But writing it out like that is a bit complex, so you might like to
set it up from a string or a text file. Then you can have a loop work
through the maze and draw the walls and pills and stuff onto the
screen.

2b and 2c; make pacman move only inside the maze
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's actually a bit tricky to go straight from the kind of movement we
have in the previous step to moving accurately and smoothly through
the maze. I found it easier to break it into two steps. First, I made
the pacman slowly jump from square to square (pacman2b) and then I
made the pacman slowly and smoothly move from square to square
(pacman2c).

In pacman games usually the pacman and ghosts are, at any one time,
exactly in the middle of a square in one dimension, and somewhere
between two in the other. You never see pacman moving diagonally off
the grid. So in my program I store the coordinates of the last maze
cell that pacman was at, a direction the pacman is moving on (one of
four compass directions), and the proportion of the journey from one
cell center to the next that the pacman has made. The pacman2b version
doesn't have the proportion of the journey variable, so the movement
is jerky. If you find the smooth movement too hard, you could stick to
jerky movement; it won't really harm the gameplay.

I found it works well if you only look at the keyboard state when the
pacman is in the middle of a cell, rather than part way between two
cells. To stick to the grid properly you need to only allow changes in
direction at cell centers anyway. Also you need to make sure that the
pacman can't walk through walls. So at each cell center my program
checks the maze data structure to make sure the pacman isn't heading
into a wall.


Phase 3; introducing the opposition
-----------------------------------

3a; a ghost to chase the pacman
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'll start with a single ghost and add multiple ghosts in the next
step. Ghost movement is very like pacman movement, so you could
duplicate the code. Only instead of looking at the keyboard, you need
some way to decide which way the ghost should move. I just have the
ghost randomly change direction sometimes, or when hitting a wall.

If you are into object oriented programming, you may be able to think
of a way to avoid duplicating the code between pacman and the ghost.

3b; multiple ghosts
~~~~~~~~~~~~~~~~~~~

Pacman with one ghost is boring; most pacman variants have around four
ghosts.

Phase 4; sorting out the gameplay
---------------------------------

4a; eating pills and scoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Being optimistic we'll introducing eating and scoring before collison
and death. So you need to check the maze data structure to figure out
what the pacman intercepts a pill, and remove the pill from the maze
data structure and screen. You can also keep score, displaying it
using the printat() command.  Pacman 4b; collison, death and levels

You need to detect when the ghosts reaches the pacman, and have some
way of letting the player know he has died. You may want to add
multiple lives. Also, when all the pills have been eaten you may want
to move the player onto a new level, with perhaps a different maze,
more ghosts or different speed settings.

When all this is done you should have a playable pacman game. But
don't stop here, because there's loads of stuff you can add on to make
it more interesting.

Phase 5; making it more fun
---------------------------

Here are some suggestions, but there's tons of other stuff you can do instead.


5a; more interesting graphics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far in my version I've used really simple graphics, so I could get
the other key things working properly. In my version I refined the
pacman and ghost graphics a little to give the game more
character. You may want to check out the range of drawing commands
available. Or, you may want to draw the graphics using external
programs and then load them using the loadimage() command. The PNG
format works well, but a number of other formats may be supported by
pygame/SDL, so try experimenting with formats.

5b; more interesting gameplay
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In my version I added power pills, which are a traditional pacman
feature which makes pacman able to kill ghosts for a limited time.

5c; sound effects!
~~~~~~~~~~~~~~~~~~

The ``play()`` command can be used to play WAV files. You can create these
using internal programs, or download them from the Internet (taking
account of copyright law of course). Carefully chosen sound effects
can really add to the atmosphere and style of a game.


Inside easygame
===============

Here were the design goals and precepts for easygame:

* Provide a single, small and consistent API. A single API in order to
  avoid the confusion of multiple packages when learning. I think
  pygame's structure is correct for serious use, but while learning it
  is often easier to have the things you use all in one place.
  
* Provide a procedural API (rather than a class based API). This is to
  avoid excluding users who don't understand classes and inheritance.

* Don't Hide The Power. Try not to get in the way when the user needs
  to do something more complex than before. Similarly, don't provide
  lots of functions which just duplice pygame functions and do nothing
  useful at all

* Immediate effect. Being able to type commands in and have them
  appear on the screen immediately is very good for
  beginners. Similarly, various initialisation stages are done
  automatically, even if occasionally this may be slightly inelegant.


* Minimal baggage, maximum leverage. The main thing that easygame
  does- keep track of dirty rectangles and a background image- is
  chosen to be as low level as possible while still hiding the
  complexity involved in smooth animation.

* Don't Fear The Type System. I was happy to take tuples and lists as
  arguments, even though it might have made the API simpler to avoid
  this. If you don't use them you end up with more parameters, and you
  don't encourage use of structured types. This is the design goal
  with which I'm least happy; I've seen other beginners APIs going to
  some lengths to allow either structured types or flat argument lists
  of primitive types; this does introduce baggage into the code which
  I didn't like, but does tend to do the "Right Thing" more often.  

* Defaults where appropriate. I put useful defaults in except where
  they are just random guesses. So there's no default position and
  radius for a circle, for example, but there is a default colour.

Easygame's code is contained mostly within single a class, called
_ScreenModel. This bundles all the state together. A small top level
routine instantiates the class, and pulls out bound methods and places
them in the module namespace. This keeps the internals of easygame
reasonably like my normal python style, while giving a procedural
API. A *power user* could always remove the few lines at the bottom of
the file if they wanted a straightforward class to subtype. The
reference documentation uses Python docstrings, and the showref method
is a very simple docstring to HTML/text converter.

The key animation routines are ''superblit()'' and
''tick()''. Superblit ends up being called for all screen operations,
and updates the pygame surfaces and rectangle lists as
appropriate. Tick does the screen update, and includes a timing
routine. ''touchedrect()'' is called by ''superblit'', or directly if the
surfaces are updated manually, and does the bookkeeping for ''tick()''.


"""



import traceback, sys, pygame
# I import pygame.locals twice.
# I prefer to resolve names explictly in the source here
# but beginners should be able to go from easygame import * and get happiness
import pygame.locals
from pygame.locals import * 
import pygame.key
import pygame.draw
import math, sys, os, threading, time, atexit
import collections
class BadArguments(Exception): pass
class FileNotFound(Exception): pass
class QuitEvent(Exception): pass
class _Colour:
    """A list of named RGB colours."""
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    black = (0,0,0)
    dark_grey = (76,76,76)
    grey = (127,127,127)
    white = (255,255,255)
    dark_red = (127,0,0)
    dark_green = (0,102,0)
    dark_blue = (0,0,127)
    light_red = (255,92,92)
    light_green = (0,255,128)
    light_blue = (0,195,255)
    yellow = (229,204,0)
    brown = (127,89,0)
    pink = (255,128,204)
    purple = (153,0,178)
    orange = (255,174,59)
    # colours from http://eies.njit.edu/~walsh and "Copyright © 2001 Kevin J. Walsh".
    black = (0, 0, 0)
    grey = (190, 190, 190)
    dimgrey = (105, 105, 105)
    lightgray = (211, 211, 211)
    lightslategrey = (119, 136, 153)
    slategray = (112, 128, 144)
    slategray1 = (198, 226, 255)
    slategray2 = (185, 211, 238)
    slategray3 = (159, 182, 205)
    slategray4 = (108, 123, 139)
    slategrey = (112, 128, 144)
    grey0 = (0, 0, 0)
    grey1 = (3, 3, 3)
    grey2 = (5, 5, 5)
    grey3 = (8, 8, 8)
    grey4 = (10, 10, 10)
    grey5 = (13, 13, 13)
    grey6 = (15, 15, 15)
    grey7 = (18, 18, 18)
    grey8 = (20, 20, 20)
    grey9 = (23, 23, 23)
    grey10 = (26, 26, 26)
    grey11 = (28, 28, 28)
    grey12 = (31, 31, 31)
    grey13 = (33, 33, 33)
    grey14 = (36, 36, 36)
    grey15 = (38, 38, 38)
    grey16 = (41, 41, 41)
    grey17 = (43, 43, 43)
    grey18 = (46, 46, 46)
    grey19 = (48, 48, 48)
    grey20 = (51, 51, 51)
    grey21 = (54, 54, 54)
    grey22 = (56, 56, 56)
    grey23 = (59, 59, 59)
    grey24 = (61, 61, 61)
    grey25 = (64, 64, 64)
    grey26 = (66, 66, 66)
    grey27 = (69, 69, 69)
    grey28 = (71, 71, 71)
    grey29 = (74, 74, 74)
    grey30 = (77, 77, 77)
    grey31 = (79, 79, 79)
    grey32 = (82, 82, 82)
    grey33 = (84, 84, 84)
    grey34 = (87, 87, 87)
    grey35 = (89, 89, 89)
    grey36 = (92, 92, 92)
    grey37 = (94, 94, 94)
    grey38 = (97, 97, 97)
    grey39 = (99, 99, 99)
    grey40 = (102, 102, 102)
    grey41 = (105, 105, 105)
    grey42 = (107, 107, 107)
    grey43 = (110, 110, 110)
    grey44 = (112, 112, 112)
    grey45 = (115, 115, 115)
    grey46 = (117, 117, 117)
    grey47 = (120, 120, 120)
    grey48 = (122, 122, 122)
    grey49 = (125, 125, 125)
    grey50 = (127, 127, 127)
    grey51 = (130, 130, 130)
    grey52 = (133, 133, 133)
    grey53 = (135, 135, 135)
    grey54 = (138, 138, 138)
    grey55 = (140, 140, 140)
    grey56 = (143, 143, 143)
    grey57 = (145, 145, 145)
    grey58 = (148, 148, 148)
    grey59 = (150, 150, 150)
    grey60 = (153, 153, 153)
    grey61 = (156, 156, 156)
    grey62 = (158, 158, 158)
    grey63 = (161, 161, 161)
    grey64 = (163, 163, 163)
    grey65 = (166, 166, 166)
    grey66 = (168, 168, 168)
    grey67 = (171, 171, 171)
    grey68 = (173, 173, 173)
    grey69 = (176, 176, 176)
    grey70 = (179, 179, 179)
    grey71 = (181, 181, 181)
    grey72 = (184, 184, 184)
    grey73 = (186, 186, 186)
    grey74 = (189, 189, 189)
    grey75 = (191, 191, 191)
    grey76 = (194, 194, 194)
    grey77 = (196, 196, 196)
    grey78 = (199, 199, 199)
    grey79 = (201, 201, 201)
    grey80 = (204, 204, 204)
    grey81 = (207, 207, 207)
    grey82 = (209, 209, 209)
    grey83 = (212, 212, 212)
    grey84 = (214, 214, 214)
    grey85 = (217, 217, 217)
    grey86 = (219, 219, 219)
    grey87 = (222, 222, 222)
    grey88 = (224, 224, 224)
    grey89 = (227, 227, 227)
    grey90 = (229, 229, 229)
    grey91 = (232, 232, 232)
    grey92 = (235, 235, 235)
    grey93 = (237, 237, 237)
    grey94 = (240, 240, 240)
    grey95 = (242, 242, 242)
    grey96 = (245, 245, 245)
    grey97 = (247, 247, 247)
    grey98 = (250, 250, 250)
    grey99 = (252, 252, 252)
    grey100 = (255, 255, 255)
    aliceblue = (240, 248, 255)
    blueviolet = (138, 43, 226)
    cadetblue = (95, 158, 160)
    cadetblue1 = (152, 245, 255)
    cadetblue2 = (142, 229, 238)
    cadetblue3 = (122, 197, 205)
    cadetblue4 = (83, 134, 139)
    cornflowerblue = (100, 149, 237)
    darkslateblue = (72, 61, 139)
    darkturquoise = (0, 206, 209)
    deepskyblue = (0, 191, 255)
    deepskyblue1 = (0, 191, 255)
    deepskyblue2 = (0, 178, 238)
    deepskyblue3 = (0, 154, 205)
    deepskyblue4 = (0, 104, 139)
    dodgerblue = (30, 144, 255)
    dodgerblue1 = (30, 144, 255)
    dodgerblue2 = (28, 134, 238)
    dodgerblue3 = (24, 116, 205)
    dodgerblue4 = (16, 78, 139)
    lightblue = (173, 216, 230)
    lightblue1 = (191, 239, 255)
    lightblue2 = (178, 223, 238)
    lightblue3 = (154, 192, 205)
    lightblue4 = (104, 131, 139)
    lightcyan = (224, 255, 255)
    lightcyan1 = (224, 255, 255)
    lightcyan2 = (209, 238, 238)
    lightcyan3 = (180, 205, 205)
    lightcyan4 = (122, 139, 139)
    lightskyblue = (135, 206, 250)
    lightskyblue1 = (176, 226, 255)
    lightskyblue2 = (164, 211, 238)
    lightskyblue3 = (141, 182, 205)
    lightskyblue4 = (96, 123, 139)
    lightslateblue = (132, 112, 255)
    lightsteelblue = (176, 196, 222)
    lightsteelblue1 = (202, 225, 255)
    lightsteelblue2 = (188, 210, 238)
    lightsteelblue3 = (162, 181, 205)
    lightsteelblue4 = (110, 123, 139)
    mediumaquamarine = (102, 205, 170)
    mediumblue = (0, 0, 205)
    mediumslateblue = (123, 104, 238)
    mediumturquoise = (72, 209, 204)
    midnightblue = (25, 25, 112)
    navyblue = (0, 0, 128)
    paleturquoise = (175, 238, 238)
    paleturquoise1 = (187, 255, 255)
    paleturquoise2 = (174, 238, 238)
    paleturquoise3 = (150, 205, 205)
    paleturquoise4 = (102, 139, 139)
    powderblue = (176, 224, 230)
    royalblue = (65, 105, 225)
    royalblue1 = (72, 118, 255)
    royalblue2 = (67, 110, 238)
    royalblue3 = (58, 95, 205)
    royalblue4 = (39, 64, 139)
    royalblue5 = (0, 34, 102)
    skyblue = (135, 206, 235)
    skyblue1 = (135, 206, 255)
    skyblue2 = (126, 192, 238)
    skyblue3 = (108, 166, 205)
    skyblue4 = (74, 112, 139)
    slateblue = (106, 90, 205)
    slateblue1 = (131, 111, 255)
    slateblue2 = (122, 103, 238)
    slateblue3 = (105, 89, 205)
    slateblue4 = (71, 60, 139)
    steelblue = (70, 130, 180)
    steelblue1 = (99, 184, 255)
    steelblue2 = (92, 172, 238)
    steelblue3 = (79, 148, 205)
    steelblue4 = (54, 100, 139)
    aquamarine = (127, 255, 212)
    aquamarine1 = (127, 255, 212)
    aquamarine2 = (118, 238, 198)
    aquamarine3 = (102, 205, 170)
    aquamarine4 = (69, 139, 116)
    azure = (240, 255, 255)
    azure1 = (240, 255, 255)
    azure2 = (224, 238, 238)
    azure3 = (193, 205, 205)
    azure4 = (131, 139, 139)
    blue = (0, 0, 255)
    blue1 = (0, 0, 255)
    blue2 = (0, 0, 238)
    blue3 = (0, 0, 205)
    blue4 = (0, 0, 139)
    cyan = (0, 255, 255)
    cyan1 = (0, 255, 255)
    cyan2 = (0, 238, 238)
    cyan3 = (0, 205, 205)
    cyan4 = (0, 139, 139)
    navy = (0, 0, 128)
    turquoise = (64, 224, 208)
    turquoise1 = (0, 245, 255)
    turquoise2 = (0, 229, 238)
    turquoise3 = (0, 197, 205)
    turquoise4 = (0, 134, 139)
    darkslategray = (47, 79, 79)
    darkslategray1 = (151, 255, 255)
    darkslategray2 = (141, 238, 238)
    darkslategray3 = (121, 205, 205)
    darkslategray4 = (82, 139, 139)
    rosybrown = (188, 143, 143)
    rosybrown1 = (255, 193, 193)
    rosybrown2 = (238, 180, 180)
    rosybrown3 = (205, 155, 155)
    rosybrown4 = (139, 105, 105)
    saddlebrown = (139, 69, 19)
    sandybrown = (244, 164, 96)
    beige = (245, 245, 220)
    brown = (165, 42, 42)
    brown1 = (255, 64, 64)
    brown2 = (238, 59, 59)
    brown3 = (205, 51, 51)
    brown4 = (139, 35, 35)
    burlywood = (222, 184, 135)
    burlywood1 = (255, 211, 155)
    burlywood2 = (238, 197, 145)
    burlywood3 = (205, 170, 125)
    burlywood4 = (139, 115, 85)
    chocolate = (210, 105, 30)
    chocolate1 = (255, 127, 36)
    chocolate2 = (238, 118, 33)
    chocolate3 = (205, 102, 29)
    chocolate4 = (139, 69, 19)
    peru = (205, 133, 63)
    tan = (210, 180, 140)
    tan1 = (255, 165, 79)
    tan2 = (238, 154, 73)
    tan3 = (205, 133, 63)
    tan4 = (139, 90, 43)
    darkgreen = (0, 100, 0)
    darkkhaki = (189, 183, 107)
    darkolivegreen = (85, 107, 47)
    darkolivegreen1 = (202, 255, 112)
    darkolivegreen2 = (188, 238, 104)
    darkolivegreen3 = (162, 205, 90)
    darkolivegreen4 = (110, 139, 61)
    darkseagreen = (143, 188, 143)
    darkseagreen1 = (193, 255, 193)
    darkseagreen2 = (180, 238, 180)
    darkseagreen3 = (155, 205, 155)
    darkseagreen4 = (105, 139, 105)
    forestgreen = (34, 139, 34)
    greenyellow = (173, 255, 47)
    lawngreen = (124, 252, 0)
    lightseagreen = (32, 178, 170)
    limegreen = (50, 205, 50)
    mediumseagreen = (60, 179, 113)
    mediumspringgreen = (0, 250, 154)
    mintcream = (245, 255, 250)
    olivedrab = (107, 142, 35)
    olivedrab1 = (192, 255, 62)
    olivedrab2 = (179, 238, 58)
    olivedrab3 = (154, 205, 50)
    olivedrab4 = (105, 139, 34)
    palegreen = (152, 251, 152)
    palegreen1 = (154, 255, 154)
    palegreen2 = (144, 238, 144)
    palegreen3 = (124, 205, 124)
    palegreen4 = (84, 139, 84)
    seagreen = (46, 139, 87)
    seagreen1 = (84, 255, 159)
    seagreen2 = (78, 238, 148)
    seagreen3 = (67, 205, 128)
    seagreen4 = (46, 139, 87)
    springgreen = (0, 255, 127)
    springgreen1 = (0, 255, 127)
    springgreen2 = (0, 238, 118)
    springgreen3 = (0, 205, 102)
    springgreen4 = (0, 139, 69)
    yellowgreen = (154, 205, 50)
    chartreuse = (127, 255, 0)
    chartreuse1 = (127, 255, 0)
    chartreuse2 = (118, 238, 0)
    chartreuse3 = (102, 205, 0)
    chartreuse4 = (69, 139, 0)
    green = (0, 255, 0)
    green1 = (0, 255, 0)
    green2 = (0, 238, 0)
    green3 = (0, 205, 0)
    green4 = (0, 139, 0)
    khaki = (240, 230, 140)
    khaki1 = (255, 246, 143)
    khaki2 = (238, 230, 133)
    khaki3 = (205, 198, 115)
    khaki4 = (139, 134, 78)
    darkorange = (255, 140, 0)
    darkorange1 = (255, 127, 0)
    darkorange2 = (238, 118, 0)
    darkorange3 = (205, 102, 0)
    darkorange4 = (139, 69, 0)
    darksalmon = (233, 150, 122)
    lightcoral = (240, 128, 128)
    lightsalmon = (255, 160, 122)
    lightsalmon1 = (255, 160, 122)
    lightsalmon2 = (238, 149, 114)
    lightsalmon3 = (205, 129, 98)
    lightsalmon4 = (139, 87, 66)
    peachpuff = (255, 218, 185)
    peachpuff1 = (255, 218, 185)
    peachpuff2 = (238, 203, 173)
    peachpuff3 = (205, 175, 149)
    peachpuff4 = (139, 119, 101)
    bisque = (255, 228, 196)
    bisque1 = (255, 228, 196)
    bisque2 = (238, 213, 183)
    bisque3 = (205, 183, 158)
    bisque4 = (139, 125, 107)
    coral = (255, 127, 80)
    coral1 = (255, 114, 86)
    coral2 = (238, 106, 80)
    coral3 = (205, 91, 69)
    coral4 = (139, 62, 47)
    honeydew = (240, 255, 240)
    honeydew1 = (240, 255, 240)
    honeydew2 = (224, 238, 224)
    honeydew3 = (193, 205, 193)
    honeydew4 = (131, 139, 131)
    orange = (255, 165, 0)
    orange1 = (255, 165, 0)
    orange2 = (238, 154, 0)
    orange3 = (205, 133, 0)
    orange4 = (139, 90, 0)
    salmon = (250, 128, 114)
    salmon1 = (255, 140, 105)
    salmon2 = (238, 130, 98)
    salmon3 = (205, 112, 84)
    salmon4 = (139, 76, 57)
    sienna = (160, 82, 45)
    sienna1 = (255, 130, 71)
    sienna2 = (238, 121, 66)
    sienna3 = (205, 104, 57)
    sienna4 = (139, 71, 38)
    deeppink = (255, 20, 147)
    deeppink1 = (255, 20, 147)
    deeppink2 = (238, 18, 137)
    deeppink3 = (205, 16, 118)
    deeppink4 = (139, 10, 80)
    hotpink = (255, 105, 180)
    hotpink1 = (255, 110, 180)
    hotpink2 = (238, 106, 167)
    hotpink3 = (205, 96, 144)
    hotpink4 = (139, 58, 98)
    indianred = (205, 92, 92)
    indianred1 = (255, 106, 106)
    indianred2 = (238, 99, 99)
    indianred3 = (205, 85, 85)
    indianred4 = (139, 58, 58)
    lightpink = (255, 182, 193)
    lightpink1 = (255, 174, 185)
    lightpink2 = (238, 162, 173)
    lightpink3 = (205, 140, 149)
    lightpink4 = (139, 95, 101)
    mediumvioletred = (199, 21, 133)
    mistyrose = (255, 228, 225)
    mistyrose1 = (255, 228, 225)
    mistyrose2 = (238, 213, 210)
    mistyrose3 = (205, 183, 181)
    mistyrose4 = (139, 125, 123)
    orangered = (255, 69, 0)
    orangered1 = (255, 69, 0)
    orangered2 = (238, 64, 0)
    orangered3 = (205, 55, 0)
    orangered4 = (139, 37, 0)
    palevioletred = (219, 112, 147)
    palevioletred1 = (255, 130, 171)
    palevioletred2 = (238, 121, 159)
    palevioletred3 = (205, 104, 137)
    palevioletred4 = (139, 71, 93)
    violetred = (208, 32, 144)
    violetred1 = (255, 62, 150)
    violetred2 = (238, 58, 140)
    violetred3 = (205, 50, 120)
    violetred4 = (139, 34, 82)
    firebrick = (178, 34, 34)
    firebrick1 = (255, 48, 48)
    firebrick2 = (238, 44, 44)
    firebrick3 = (205, 38, 38)
    firebrick4 = (139, 26, 26)
    pink = (255, 192, 203)
    pink1 = (255, 181, 197)
    pink2 = (238, 169, 184)
    pink3 = (205, 145, 158)
    pink4 = (139, 99, 108)
    red = (255, 0, 0)
    red1 = (255, 0, 0)
    red2 = (238, 0, 0)
    red3 = (205, 0, 0)
    red4 = (139, 0, 0)
    tomato = (255, 99, 71)
    tomato1 = (255, 99, 71)
    tomato2 = (238, 92, 66)
    tomato3 = (205, 79, 57)
    tomato4 = (139, 54, 38)
    darkorchid = (153, 50, 204)
    darkorchid1 = (191, 62, 255)
    darkorchid2 = (178, 58, 238)
    darkorchid3 = (154, 50, 205)
    darkorchid4 = (104, 34, 139)
    darkviolet = (148, 0, 211)
    lavenderblush = (255, 240, 245)
    lavenderblush1 = (255, 240, 245)
    lavenderblush2 = (238, 224, 229)
    lavenderblush3 = (205, 193, 197)
    lavenderblush4 = (139, 131, 134)
    mediumorchid = (186, 85, 211)
    mediumorchid1 = (224, 102, 255)
    mediumorchid2 = (209, 95, 238)
    mediumorchid3 = (180, 82, 205)
    mediumorchid4 = (122, 55, 139)
    mediumpurple = (147, 112, 219)
    mediumpurple1 = (171, 130, 255)
    mediumpurple2 = (159, 121, 238)
    mediumpurple3 = (137, 104, 205)
    mediumpurple4 = (93, 71, 139)
    lavender = (230, 230, 250)
    magenta = (255, 0, 255)
    magenta1 = (255, 0, 255)
    magenta2 = (238, 0, 238)
    magenta3 = (205, 0, 205)
    magenta4 = (139, 0, 139)
    maroon = (176, 48, 96)
    maroon1 = (255, 52, 179)
    maroon2 = (238, 48, 167)
    maroon3 = (205, 41, 144)
    maroon4 = (139, 28, 98)
    orchid = (218, 112, 214)
    orchid1 = (255, 131, 250)
    orchid2 = (238, 122, 233)
    orchid3 = (205, 105, 201)
    orchid4 = (139, 71, 137)
    plum = (221, 160, 221)
    plum1 = (255, 187, 255)
    plum2 = (238, 174, 238)
    plum3 = (205, 150, 205)
    plum4 = (139, 102, 139)
    purple = (160, 32, 240)
    purple1 = (155, 48, 255)
    purple2 = (145, 44, 238)
    purple3 = (125, 38, 205)
    purple4 = (85, 26, 139)
    thistle = (216, 191, 216)
    thistle1 = (255, 225, 255)
    thistle2 = (238, 210, 238)
    thistle3 = (205, 181, 205)
    thistle4 = (139, 123, 139)
    violet = (238, 130, 238)
    antiquewhite = (250, 235, 215)
    antiquewhite1 = (255, 239, 219)
    antiquewhite2 = (238, 223, 204)
    antiquewhite3 = (205, 192, 176)
    antiquewhite4 = (139, 131, 120)
    floralwhite = (255, 250, 240)
    ghostwhite = (248, 248, 255)
    navajowhite = (255, 222, 173)
    navajowhite1 = (255, 222, 173)
    navajowhite2 = (238, 207, 161)
    navajowhite3 = (205, 179, 139)
    navajowhite4 = (139, 121, 94)
    oldlace = (253, 245, 230)
    whitesmoke = (245, 245, 245)
    gainsboro = (220, 220, 220)
    ivory = (255, 255, 240)
    ivory1 = (255, 255, 240)
    ivory2 = (238, 238, 224)
    ivory3 = (205, 205, 193)
    ivory4 = (139, 139, 131)
    linen = (250, 240, 230)
    seashell = (255, 245, 238)
    seashell1 = (255, 245, 238)
    seashell2 = (238, 229, 222)
    seashell3 = (205, 197, 191)
    seashell4 = (139, 134, 130)
    snow = (255, 250, 250)
    snow1 = (255, 250, 250)
    snow2 = (238, 233, 233)
    snow3 = (205, 201, 201)
    snow4 = (139, 137, 137)
    wheat = (245, 222, 179)
    wheat1 = (255, 231, 186)
    wheat2 = (238, 216, 174)
    wheat3 = (205, 186, 150)
    wheat4 = (139, 126, 102)
    white = (255, 255, 255)
    blanchedalmond = (255, 235, 205)
    darkgoldenrod = (184, 134, 11)
    darkgoldenrod1 = (255, 185, 15)
    darkgoldenrod2 = (238, 173, 14)
    darkgoldenrod3 = (205, 149, 12)
    darkgoldenrod4 = (139, 101, 8)
    lemonchiffon = (255, 250, 205)
    lemonchiffon1 = (255, 250, 205)
    lemonchiffon2 = (238, 233, 191)
    lemonchiffon3 = (205, 201, 165)
    lemonchiffon4 = (139, 137, 112)
    lightgoldenrod = (238, 221, 130)
    lightgoldenrod1 = (255, 236, 139)
    lightgoldenrod2 = (238, 220, 130)
    lightgoldenrod3 = (205, 190, 112)
    lightgoldenrod4 = (139, 129, 76)
    lightgoldenrodyellow = (250, 250, 210)
    lightyellow = (255, 255, 224)
    lightyellow1 = (255, 255, 224)
    lightyellow2 = (238, 238, 209)
    lightyellow3 = (205, 205, 180)
    lightyellow4 = (139, 139, 122)
    palegoldenrod = (238, 232, 170)
    papayawhip = (255, 239, 213)
    cornsilk = (255, 248, 220)
    cornsilk1 = (255, 248, 220)
    cornsilk2 = (238, 232, 205)
    cornsilk3 = (205, 200, 177)
    cornsilk4 = (139, 136, 120)
    gold = (255, 215, 0)
    gold1 = (255, 215, 0)
    gold2 = (238, 201, 0)
    gold3 = (205, 173, 0)
    gold4 = (139, 117, 0)
    goldenrod = (218, 165, 32)
    goldenrod1 = (255, 193, 37)
    goldenrod2 = (238, 180, 34)
    goldenrod3 = (205, 155, 29)
    goldenrod4 = (139, 105, 20)
    moccasin = (255, 228, 181)
    yellow = (255, 255, 0)
    yellow1 = (255, 255, 0)
    yellow2 = (238, 238, 0)
    yellow3 = (205, 205, 0)
    yellow4 = (139, 139, 0)
    copper = (184, 115, 51)
    gold = (205, 127, 50)
    silver = (230, 232, 250)
    
    def __iter__(self):
        return iter([col for col in dir(self) if col[0] != '_'])
    def __call__(self, k):
        if type(k) == type(''):
            return getattr(self, k)
        if type(k) == type((1,2)) and len(k) in [3,4]:
            return k

Colour = _Colour()

def clipline(pos0, pos1, cr):
    # Cohen-Sutherland line clipping
    def outcode(pos,cr):
        code = 0
        if pos[1] < cr.top: code += 1
        if pos[1] >= cr.bottom: code += 2
        if pos[0] < cr.left: code += 4
        if pos[0] >= cr.right: code += 8
        return code
    oc0 = outcode(pos0,cr)
    oc1 = outcode(pos1,cr)
    done = 0
    while not done:
        if oc0==0 and oc1 == 0:
            accept =1
            done = 1
        elif oc0 & oc1 != 0:
            # shared outside bit
            accept = 0
            done =1
        else:
            # need to move one edge in
            if oc0:
                ocout = oc0
            else:
                ocout = oc1
            assert ocout != 0
            # now ocout is guaranteed to be outside
            x0, y0 = pos0
            x1, y1 = pos1
            if ocout & 1: # cross cr.top
                assert y1 != y0
                npos = (x0+(x1-x0)*(cr.top-y0)/(y1-y0), cr.top)
            if ocout & 2: # cross cr.bottom
                assert y1 != y0
                npos = (x0+(x1-x0)*(cr.bottom-1-y0)/(y1-y0), cr.bottom-1)
            if ocout & 4: # cross cr.left
                assert x1 != x0
                npos = (cr.left, y0+(y1-y0)*(cr.left-x0)/(x1-x0))
            if ocout & 8: # cross cr.right
                assert x1 != x0
                npos = (cr.right-1, y0+(y1-y0)*(cr.right-1-x0)/(x1-x0))
            if ocout == oc0:
                #print pos0,pos1,'->',npos,pos1
                pos0 = npos
                oc0 = outcode(pos0,cr)
            else:
                #print pos0,pos1,'->',pos0,npos
                pos1 = npos
                oc1 = outcode(pos1,cr)
    return pos0, pos1, accept

def clippoly(poslist, cr):
    """
    >>> cr = Rect( (100,100), (200,200) )
    >>> clippoly( [], cr)
    []
    >>> clippoly([(0,0)], Rect( (100,100), (100,100) ) )
    []
    >>> clippoly([(0,0), (400,0), (0,250)], Rect( (100,100), (100, 100) ) )
    [(199, 125), (100, 187), (100, 100), (199, 100)]

    In some cases the algorithm introduces spurious extra edges:
    >>> clippoly([(150,150),(350,150)], Rect( (100,100), (100,100) ))
    [(199, 150), (199, 150), (150, 150)]
    """
    # Sutherland-Hodgman polygon clipping
    for (axis, oaxis, sense, val) in [
        (0,1, -1, cr.left),
        (0,1, 1, cr.right-1),
        (1,0, -1, cr.top),
        (1,0, 1, cr.bottom-1)]:
        nposlist = []
        prevout = 0
        prevpos = None
        if poslist == []: return poslist
        for pos in poslist+[poslist[0]]:
            hereout = (sense > 0 and pos[axis] > val) or (sense < 0 and pos[axis] < val)
            if prevpos != None:
                if (not prevout) and (not hereout):
                    # completely in
                    nposlist.append(pos)                
                elif not(prevout and hereout):
                    ipos = [0,0]
                    ipos[axis] = val
                    assert pos[axis] != prevpos[axis]
                    ipos[oaxis] = prevpos[oaxis] + (pos[oaxis]-prevpos[oaxis])*(val-prevpos[axis])/(pos[axis]-prevpos[axis])
                    nposlist.append(tuple(ipos))
                    if not hereout:
                        nposlist.append(pos)
            prevout = hereout
            prevpos = pos
        poslist = nposlist

    return poslist


def rotozoompositions(positions,angle,zoom):
    cx,cy = 0, 0
    for pos in positions:
        cx += pos[0]
        cy += pos[1]
    cx /= len(positions)
    cy /= len(positions)
    angle = -(angle  *math.pi * 2) / 180.0
    ix, iy = zoom*math.cos(angle), zoom*math.sin(angle)
    jx, jy = -zoom*math.sin(angle), zoom*math.cos(angle)
    npositions = []
    for pos in positions:
        x, y= pos[0]-cx, pos[1]-cy
        npos = cx+x*ix+y*jx, cy+x*iy+y*jy
        npositions.append ( npos)
    return npositions        


def _preform(doc):
    q = doc.find('>>>')
    if q != -1:
        doc = doc[:q] + '<PRE>'+doc[q:]+'</PRE>'
    return doc

def gendoc(clss=None, html=0, pre='', intro=1):
    def dedent(s):
        lines= s.split('\n')
        dent = ''
        for ch in lines[1]:
            if not ch.isspace(): break
            dent += ch
        o = []
        for line in lines:
            if line.startswith(dent):
                o.append(line[len(dent):])
            else:
                o.append(line)
        return '\n'.join(o)

    if clss is None:
        cl = [_ScreenModel, Pos, Sprite]
    else:
        cl = [clss]
    l = []
    if intro and not html:
        import easygame
        l.append(dedent(easygame.__doc__))
    for clss in cl:
        cmds = dir(clss)
        pre = clss.__name__
        cmds.sort()
        lines = None
        ofilename = None
        if html:
            l.append(_preform(clss.__doc__))
        else:
            import easygame
            #print >>sys.stderr, clss, `clss.__doc__`
            l.append(dedent(clss.__doc__))
        ncmds = []
        for cmd in cmds:
            if cmd == '__init__': ncmds = [cmd] + ncmds
            else:
                ncmds = ncmds + [cmd]
        for cmd in ncmds:
            if cmd[0] == '_' and cmd[-1] != '_': continue
            method = getattr(clss, cmd)
            if not hasattr(method, '__doc__'): continue
            doc = method.__doc__
            func = ''
            try:
                # this is a hack to get the function definition out
                # by introspection, and assuming some stuff about the code layout
                # not necessarily portable between python versions; works on python 2.1
                filename = method.__func__.__code__.co_filename
                if filename != ofilename:
                    lines = open(filename, 'r').readlines()
                    ofilename = filename
                func = lines[method.__func__.__code__.co_firstlineno-1][:-1]
                f = func.find('(self')
                if f== -1:
                    func = ''
                else:
                    if func[f+5] == ')':
                        func = cmd+'()'
                    else:
                        body = func[f+6:]
                        if body[0] == ' ': body = body[1:]
                        func = cmd+'('+body           
            except: pass
            if func == '': func = cmd
            if doc:
                if html:
                    l.append('<B>%s%s</B><P/><BLOCKQUOTE>%s</BLOCKQUOTE><BR>' % (pre, func, _preform(doc)))
                else:
                    t = pre+'.'+func
                    if t[-1] == ':': t = t[:-1]
                    l.append('%s\n%s\n%s\n' % (t,len(t)*'-', doc))
    return '\n'.join(l)

def showref(html=0):
    d = ''
    for (clss, title, pre) in [
        (_ScreenModel, 'Basic easygame operations (the _ScreenModel class)', ''),
        (Pos, "The Pos class", "Pos."),
        (Sprite, "The Sprite class", "Sprite.")]:
        if html:
            d += '<H3>'+title+'</H3>\n' + gendoc(clss, 1, pre, intro=0)
        else:
            d += title+'\n'+('*'*len(title))+'\n'+gendoc(clss, 0, pre, intro=0)
    return d

class OffScreen(Exception): pass

class Sprite:
    """
    The Sprite class
    ================

    Key to the optional Sprite subsystem. You can use
    the Sprite class without subclassing it, but subclassing can be used
    to change methods which you don't find flexible enough.

    >>>
    
    """
    def __init__(self, initpos, initvel, drawop=None, *exl, **exk):
        """ Create a sprite at initpos moving along vector initvel,
        drawn by drawop. The rest of the arguments are passed to drawop.
        drawop will be given a pos as first argument, and temp=1 in the
        keyword arguments. It should return a boundingrect. """
        self.exl = exl
        self.exk = exk
        self.exk['temp'] = 1
        self.pos = Pos(initpos)
        self.vel = Pos(initvel)
        self.drawop = drawop
        self.rect = None
        self.donerender = 0
        addsprite(self)
    def draw(self):
        """ Called by spritetick() when the sprite needs to be updated.
        Subclassses must set self.rect to the bounding rect and
        self.donerender to one.
        """
        if self.drawop == None: pass
        try:
            self.rect =  self.drawop(*[self.pos] + list(self.exl), **self.exk)
            self.donerender = 1
            return self.rect
        except OffScreen: pass
    def tick(self,t):
        """ Called by spritetick() with the mean frame time as an argument.
        """
        self.pos += self.vel * t
        self.draw()
    def __repr__(self):
        """ represent object """
        r = [repr(self.pos), repr(self.vel)]
        try:
            r +=[ self.drawop.__name__]
        except:
            r += [repr(self.drawop)]
        for arg in self.exl: r += [repr(arg)]
        ks = list(self.exk.keys())
        ks.sort()
        for arg in ks:
            r += [arg + '-' + repr(self.exk[arg])]
        return 'Sprite('+', '.join(r)+')'
    def overlapping(self, other):
        """ return true if sprite overlaps with other (a sprite or rectangle ).
        Designed for the user to call, i.e.

        if sprite1.overlapping(sprite2):
           # collison handler

        """
        try:
            if self.donerender == 0:
                print('Extra draw')
                self.draw()
            if isinstance(other, Sprite):
                if other.donerender == 1:
                    other = other.rect
                else:
                    return 0
            if other == None: return 0
            return self.rect.colliderect(other)
        except:
            print('exc')
            pass
            

class _ScreenModel:
    """
    The ScreenModel class
    =====================
    
    The ScreenModel class, the main class in easygame. The methods of
    this class are available as functions in the easygame namespace.
    
    ScreenModel provides some wrappers around the basic pygame APIs
    to hopefully make them easier to use.

    In particular, the singleton instance of this class keeps track
    of a background surface, so that objects can be drawn temporarily
    on top of the background and later the background restored (cleartemp)
    This provides an easy way to do movement.

    Also, all the drawing operations maintain a dirty rectangles list and
    by default (unless batching mode is enabled), cause updates to be
    exposed straight to the screen.

    >>> from easygame import *
    >>> # your easygame commands go here; a window appears for you automatically
    """
    def __init__(self, surf=None):
        pygame.init()
        modes = pygame.display.list_modes()
        self.screen = None
        if surf:
            self.setsurf(surf)
        else:
            self.setmode( (640,480) ) # calls self.setsurf
        self.batching = 0
        self.fonttable = {}
        self.imagecache = {}
        self.soundcache = None
        self.tcache = None # caching of text rendering for onlysize of printat
        self.scache = None # caching of surface for onlysize of superblit
        self.sprites = []
        self.defaultcolour = Colour.white
        self.intouch = 0
        self.shutdown = False
    def _loadimage(self,filename):
        """ internal function to load an image and cache it """
        if filename in self.imagecache: return self.imagecache[filename]
        if not os.path.exists(filename):
            raise FileNotFound(filename)
        surf = pygame.image.load(filename)
        surf.set_colorkey(surf.get_at((0,0)), pygame.locals.RLEACCEL)
        image = surf.convert()
        self.imagecache[filename] = image
        return image
    def _loadsound(self,filename):
        """ internal function to load a sound file """
        import pygame.mixer
        if self.soundcache == None:
            self.soundcache = {}
            pygame.mixer.init()
        if filename in self.soundcache: return self.soundcache[filename]
        sound = pygame.mixer.Sound(filename)
        self.soundcache[filename] = sound
        return sound
    def closedown(self):
        pygame.display.quit()
        del self.background
        del self.screen
        self.shutdown = True
    def resettime(self):
        """ reset the timing system. Should be called at the start
        of drawing a sequence of similar frames at a similar rate,
        so that the timing system can react. """
        self.lttime = pygame.time.get_ticks()
        self.tlist = []
    def _colour(self,col):
        """Convert col to a tuple"""
        if col is None: return self.defaultcolour
        else: return Colour(col)
    def setcolour(self, col):
        """Set the default drawing colour.

        col should be an (R,G,B) (values out of 256) tuple or a
        string such as 'red', 'green', 'blue', 'black', 'dark_grey', 'grey',
        'white', 'dark_red', 'dark_green', 'dark_blue', 'light_red',
        'light_green', 'light_blue', 'yellow', 'brown', 'pink',
        'purple', or 'orange', or many others.
        """
        self.defaultcolour = self._colour(col)
    def setmode(self, size, fullscreen=0,depth=0, flags=0):
        """ set screen mode to the given size.
        If argument fullscreen is set to true, display full screen. In that
        case size had better be a suitable video card resolution.
        If depth is set, try to get that number of bits per pixel.
        If flags is set, set those flags. See the documentation for pygame.display.set_mode

        Automatically sets the drawing clipping rectangle to the whole of the
        new screen area.
        """
        
        if fullscreen:
            flags |= pygame.locals.FULLSCREEN
        if self.screen != None:
            pass
        screen = pygame.display.set_mode(size, flags,depth)
        self.setsurf(screen)
    def setsurf(self, surf):
        """ set surf as the output surface """
        size = surf.get_size()
        self.screen = surf
        self.screenrect = Rect((0,0),size)
        self.background = pygame.Surface(size, depth=surf.get_bitsize())
        self.dirty = []
        self.fgrects = {}
        self.resettime()
        self.cliprect = self.screenrect
    def setclipping(self, rect=None):
        """ set the drawing clipping rectangle to rect.
        rect is automatically clipped to fit onto the screen
        If rect is None then allowing drawing over the whole screen.
        Returns the actual new clipping rectangle. """
        if type(rect) == type(None) and rect == None:
            self.cliprect = self.screenrect
        else:
            self.cliprect = self.screenrect.clip(Rect(rect))
        return self.cliprect
    def getscreensurface(self):
        """ return the screen surface (not a copy). Make sure you call updaterect
        if you modify the surface.
        """
        return self.screen
    def getbackgroundsurface(self):
        """ return the background surface (not a copy). Make
        sure you call updaterect if you modify the surface.
        """
        return self.background
    def getscreensize(self):
        """ return the screen size (as a Pos) """
        return Pos(self.screenrect.width, self.screenrect.height)
    def getscreenwidth(self):
        """ return the screen width. """
        return self.screenrect.width
    def getscreenheight(self):
        """ return the screen height. """
        return self.screenrect.height
    def setbatching(self, batching):
        """ if batchingO is true, request that subsequent screen updates are not posted to
        the screen immediately, but instead wait for the next tick"""
        self.batching = batching
    def superblit(self, destpos, img, srcrect=None,temp=0,topleft=0,angle=0,zoom=1,onlysize=0,onlygetsurface=0, alpha=None):
        """ place img on to the screen at destpos. destpos specifies the
        middle of the image unless topleft is set to true.
        If srcrect is specified, copy only that part of img otherwise take
        the whole lot (default).
        If onbg is specified false, make the blit disappear after the next
        tick.
        If temp is true, make this drawing temporary.
        Angle and zoom can be used to rotate and zoom on the image.
        onlysize can be used to return the size of the transformed image without doing anything to the screen.
        onlygetsurface can be used to return the pygame Surface of the transformed image without doing anything to the screen.
        It's called superblit because it keeps track of dirty rectangles,
        handles a bg/fg model, and can call tick automatically.
        """
        #print 'superblit',destpos,img,srcrect,temp,topleft,angle,zoom
        destpos=  (int(destpos[0]), int(destpos[1]))
        if type(srcrect) == type(None):
            srcrect = img.get_rect()
        if (angle !=0 or zoom!=1):
            oimg = img
            if self.scache == (img,angle,zoom,srcrect):
                img = self.scacheimg
                srcrect = img.get_rect()
            else:
                import pygame
                if srcrect.size != img.get_size():
                    tempsurf = pygame.Surface( (srcrect.width,srcrect.height) )
                    tempsurf.blit(img,(0,0), srcrect)
                    img = tempsurf
                import pygame.transform
                img = img.convert_alpha()
                img = pygame.transform.rotozoom(img, angle,zoom)
                self.scache = (oimg,angle,zoom,srcrect)
                self.scacheimg = img
                srcrect = img.get_rect()
        if not topleft:
            destpos = (destpos[0] - (srcrect.width/2), destpos[1] - (srcrect.height/2))
        origdestrect = Rect(destpos, srcrect.size)
        destrect = self.cliprect.clip(origdestrect)
        if destrect != origdestrect:
            deltapos = (destrect.left - origdestrect.left, destrect.top - origdestrect.top)
            deltasize = (destrect.width - origdestrect.width, destrect.height - origdestrect.height)
            destpos = (destpos[0]+deltapos[0], destpos[1] + deltapos[1])
            srcrect = Rect((srcrect.left+deltapos[0], srcrect.top+deltapos[1]),
                           (srcrect.width + deltasize[0], srcrect.height+deltasize[1]))
        if onlysize: return destrect
        if onlygetsurface: return img
        if alpha:
            img.set_alpha(alpha)
        if not temp:
            self.background.blit(img, destpos, srcrect)
        rect = self.screen.blit(img, destpos, srcrect)
        self.touchedrect(rect, temp)
        return rect
    def touchedrect(self, rect, temp=0):
        """ Does the bookkeeping to reflect that the screen and/or background
        have been updated. 
        If temp is false, assume the background has changed. All the
        drawing operations including superblit call this routine, so user
        code need only call it when it has modified the screen or background
        directly.
        """
        if self.intouch == 1: return
        self.intouch = 1
        assert isinstance(rect, Rect), rect
        self.dirty.append(rect)
        if temp:
            if temp not in self.fgrects: self.fgrects[temp] = []
            self.fgrects[temp].append(rect)
        if self.batching==0: self.tick()
        #self.line( rect.topleft, rect.bottomright, col='red', temp=1)
        #self.line( rect.topright, rect.bottomleft, col='red', temp=1)        
        self.intouch =0
        return rect
    def tick(self, fps=None, rough=1, quick=0):
        """ update the screen and timing system, and any sprites

        If fps is set, run at most that number of ticks per second.
        If rough is not set or is set to true, use rough waiting when recovering. Normally true.
        """
        if self.shutdown:
            return
        pygame.event.pump()
        # it shouldn't be necessary to exit at this point, but if we
        # are called from the idlefork socket thread and call
        # pygame.display.update, we get a problem inside pygame
        if quick: return
        
        pygame.display.update(self.dirty)
        self.dirty=[]
        if quick: return
        if fps:
            ftime = 1000.0/fps
            t = pygame.time.get_ticks()
            deltat = t - self.lttime
            # fps debugging
            #self.printat((100,100),fps,deltat,ftime,ftime-deltat,temp=1); pygame.display.update(self.dirty)
            if ftime - deltat > 0.0:
                self.pause(ftime - deltat,rough=rough)
        t = pygame.time.get_ticks()
        deltat = t - self.lttime        
        self.lttime = t        
        dt = deltat / 1000.0
        self.tlist = self.tlist[-50:] + [dt]
        tac = 0
        for t in self.tlist:
            tac += t
        tav = tac/max(len(self.tlist),1)
        return tav
    def cleartemp(self,temp=None):
        """ remove temporary drawing. If temp is set, remove only
        temporary drawing done with temp set to the same value, otherwise
        remove all temporary drawing. """
        if temp==None:
            ks = list(self.fgrects.keys())
        else:
            ks = []
            if temp in self.fgrects:
                ks = [temp]
        for k in ks:
            for rect in self.fgrects[k]:
                self.superblit(rect.topleft, self.background, srcrect=rect,topleft=1)
            self.fgrects[k] = []
    def clearscreen(self, bg = (0,0,0), temp=0):
        """ clear the screen. bg can be used to specify the colour, which
        defaults to black. If temp is true, make this drawing temporary."""
        self.cleartemp()
        if temp == 1: return
        # use the fast fill to clear the background
        self.background.fill(bg, self.cliprect)
        self.screen.fill(bg,self.cliprect)
        self.touchedrect(self.cliprect)
        return self.screenrect
    def plotimage(self, pos, filename, **kwargs):
        """ load image from filename, and place it onto the screen at pos
        pos should be a 2-integer sequence.
        Normally pos specifies the position of the middle of the image.

        topleft if set to true specifies pos refers to the topleft of the image rather than the center.
        temp if set to true makes the drawing temporary so that cleartemp restores what was their before.
        onlysize if set to true disables the drawing and returns the size of the drawing as a Rectangle
        onlygetsurface if set to true disables the drawing and returns the image as a pygame Surface.
        angle specifies the angle the image is plotted at 
        zoom specifies the zoom factor
        alpha specifies the transparency (0=clear 255=opaque None=opaque)
        """
        img = self._loadimage(filename)
        return self.superblit(*[pos,img], **kwargs)
    def printat(self, pos, *args, **kwargs):
        """ place some text on the screen at pos. Interprets (non keyword)
        arguments like print does; i.e. converts them to strings if necessary
        and then displays them separated by spaces.

        font sets the filename of the font file, default some fairly plain font (Verdana).
        pointsize sets the number of points in the pixel, default 20.
        fg sets the foreground colour 
        bg sets the background colour (default transparent)
        topleft if set to true specifies pos refers to the topleft of the text rather than the center.
        temp if true makes the drawing temporary.
        onlysize if set to true disables the drawing and returns the size of the text as a Rectangle
        onlygetsurface if set to true disables the drawing and returns the image as a pygame Surface.

        angle specifies the angle the text is at.
        zoom specifies the zoom factor (though using a larger pointsize will give smoother text)      
        alpha specifies the transparency (0=clear 255=opaque 255=opaque)
        
        size if specified specifies the maximum width and height of the text;
        the font size is adjusted such that the text does not exceed this
        width and height. If you set both pointsize and size you get a
        BadArguments exception.
                
        printat returns the bounding box of the drawn text.
        """
        font = kwargs.pop('font', 'Verdana')
        pointsize = kwargs.pop('pointsize', None)
        fg = kwargs.pop('fg', self.defaultcolour)
        bg = kwargs.pop('bg',None)
        topleft = kwargs.pop('topleft',0)
        onlysize = kwargs.pop('onlysize',0)
        onlygetsurface = kwargs.pop('onlygetsurface',0)
        temp = kwargs.pop('temp',0)
        angle = kwargs.pop('angle',0)
        zoom = kwargs.pop('zoom',1)
        alpha = kwargs.pop('alpha', None)
        size = kwargs.pop('size', None)                
        if fg is None:
            fg = self.defaultcolour
        if pointsize is None and size is None:
            pointsize = 20
        if size:
            size = Pos(size)
        fg = self._colour(fg)
        if not bg is None:
            bg = self._colour(bg)
        # at this point all the arguments in the list in the previous
        # block have been defined as local variables
        if kwargs != {}:
            raise BadArguments(kwargs)
        targ = []
        for arg in args:
            if type(arg) == type(''): targ.append(arg)
            else: targ.append(repr(arg))
        text = ' '.join(targ)
        if text == '': return
        import pygame.font
        if size and pointsize:
            raise BadArguments({size:size,pointsize:pointsize}) # you specified both size and pointsize
        if pointsize is None:
            pointsize = min(size[1], size[0] / len(text)) 
        iterations = 0
        while True:        
            tdes=  (text,font,pointsize,fg,bg)
            pointsize = int(pointsize)
            if self.tcache == tdes:
                tsurf = self.tcachesurf
            else:
                if (font, pointsize) not in self.fonttable:
                    self.fonttable[ (font, pointsize) ] = pygame.font.SysFont(font, pointsize)
                font = self.fonttable[ (font, pointsize) ]
                if bg == None:
                    tsurf = font.render(text, 1, fg)
                else:
                    tsurf = font.render(text, 1, fg, bg)
            if size is None:
                break    
            print(pointsize, tsurf.get_rect().width, tsurf.get_rect().height, size)
            w = tsurf.get_rect().width
            ratio = w / size[0]
            if iterations > 5:
                if ratio < 1:
                    break
                else:
                    pointsize /= 4
            iterations += 1
            if ratio > 0.95:
                break
            else:
                pointsize /= ratio*1.1
                
            
        self.tcache = tdes
        self.tcachesurf = tsurf
        return self.superblit(pos,tsurf,temp=temp,topleft=topleft,
                              onlysize=onlysize,
                              onlygetsurface=onlygetsurface,
                              angle=angle,zoom=zoom, alpha=alpha)
    def _drawop(self, op, *args, **kwargs):
        args = list(args)
        rect = op(*[self.screen]+args)
        temp = 0
        if 'temp' in kwargs: temp = kwargs['temp']
        if 'rect' in kwargs: rect = kwargs['rect']
        if not temp:
            op(*[self.background]+args)            
        return  self.touchedrect(rect,temp=temp)
    def circle(self, pos, radius, col=None, width=0, temp=0,angle=0,zoom=1):
        """ draw a circle centred at pos and of the given radius
        If width is zero or unspecified, draw a solid circle
        Otherwise draw a circle of the given width.

        If ``temp`` is true, then draw circle temporarily, recording what
        is undernath so ``cleartemp`` can remove it.

        Returns the bounding rectangle of the circle.        

        angle specifies the angle the circle is plotted at, but is included
        for completeness and doesn't actually affect the appearance of the circle.
        zoom specifies the zoom factor

        """
        col = self._colour(col)
        r = int(radius)
        if r < radius: r+=1
        cr = self.cliprect
        if pos[0] - r < cr.left or pos[0] + r > cr.right or pos[1] - r < cr.top or pos[1] + r > cr.bottom:
            return ellipse(Rect(pos[0]-r, pos[1]-r, 2*r, 2*r), col=col,width=width,temp=temp)
        else:
            return self._drawop(pygame.draw.circle,
                         col,Pos(pos).tointeger(),r-1,width,
                         temp=temp,rect=Rect((int(pos[0]-r),int(pos[1]-r)),(r*2,r*2)))
    def arc(self, pos0, pos1, x, col=None, width=1, debug=0, steps=None,
            temp=0):
        """
        Draw an arc from ``pos0`` to ``pos1`` in colour ``col``
        width ``width``.

        If ``x`` is a number, draw arc that extends to the left (as you go
        from pos0 to pos1) by ``x`` units, in colour ``col``.  Otherwise if
        ``x`` is a coordinate (something that can be interpreted by Pos, ie a
        Pos instance, a 2-tuple or 2-list), the arc also passes through
        ``x``.  Otherwise you get a TypeError.

        If ``debug`` is true, show working constructions.
        If ``steps`` is set, draw arc with that number of sides. (Small odd
        numbers look a bit odd).

        If ``temp`` is true, then draw circle temporarily, recording what
        is undernath so ``cleartemp`` can remove it.
        
        """
        pos0, pos1, = Pos(pos0), Pos(pos1)
        if type(x) in [type(1), type(1.0)]:
            if abs(x) < 0.000001:
                return line(pos0, pos1, width=width, col=col)

            midpoint = (pos0 + pos1)/2
            vec = pos1 - pos0 # vector along line
            unitvec = vec / vec.magnitude # unit vector along line
            orthvec = Pos(magnitude=1, direction=unitvec.direction+90)
            pos2 = midpoint+orthvec * x
        else:
            pos2 = Pos(x)
        if debug:
            self.circle(pos2, 10, width=2, col=Colour.yellow)
        try:
            origin = circleoriginfromthreepoints(pos0, pos1, pos2)
        except ZeroDivisionError: # indicates the points are co-linear 
            return line(pos0, pos1, width=width, col=col, temp=temp)
        r = origin.distanceto(pos0)
        t0 = ((pos0 - origin).direction)%360
        t1 = ((pos1 - origin).direction)%360
        t2 = ((pos2 - origin).direction)%360
        if debug:
            self.line(origin, origin + Pos(magnitude=20, direction=t0),
                      col=Colour.red)
            self.line(origin, origin + Pos(magnitude=20, direction=t1),
                      col=Colour.blue)
        segments = []
        for angle in anglerange(t0,t2,t1, steps, r):
            segments.append ( Pos(magnitude = r, direction=angle) + origin)
        return self.lines(segments, width=width, col=col, temp=temp)

    def ellipse(self, rect, col=None, width=0,temp=0,angle=0,zoom=1):
        """
        Draw an ellipse touching the edges of rect.
        If ``width`` is zero or unspecified, draw a solid ellipse otherwise
        draw a ellipse of the given width.
        If ``temp`` is true, then draw ellipse temporarily.
        If ``angle`` is set, rotate the ellipse by that angle.
        If ``onlysize`` is set, don't actually draw the ellipse.

        ``angle`` specifies the angle the ellipse is plotted at.
        
        ``zoom`` specifies the zoom factor
        
        Returns the bounding rectangle of the ellipse.        
        """
        col = self._colour(col)
        if zoom != 1:
            rect.inflate(rect.width*(zoom-1), rect.height*(zoom-1))
        pos = rect.center
        colrect = self.cliprect.clip(rect)
        if colrect.width == 0 or colrect.height == 0: return Rect(0,0,0,0)
        if colrect == rect and angle==0:
            return self._drawop(pygame.draw.ellipse,
                                 col,rect,width, temp=temp)
        else:
            # ellipse only partially out, or rotated
            sides = 4 + ( rect.width + rect.height)//4
            theta = 0
            thetainc = math.pi * 2 / sides
            pts = []
            for i in range(sides):
                pts.append ( (pos[0]+(rect.width/2.0)*math.sin(theta),
                              pos[1]+(rect.height/2.0)*math.cos(theta)) )
                theta += thetainc
            # let the polygon do the clipping (could be improved)
            return self.polygon( pts, col=col, width=width,
                                 temp=temp, angle=angle)

    def line(self,pos0,pos1, col=None,width=1,temp=0,angle=0,zoom=1):
        """
        Draws a line from ``pos1`` to ``pos2``.

        Line width is ``width`` or defaults to one pixel.
        
        If ``temp`` is true, then draw line temporarily.
        angle specifies the angle the line is rotated through
        zoom specifies the zoom factor
        (angle and zoom operate around the center of the line)        
        Returns the bounding rectangle of the line.        
        """
        col = self._colour(col)
        #print 'Line',pos0,pos1
        if angle !=0 or zoom != 1:
            (pos0, pos1) = rotozoompositions([pos0,pos1],angle,zoom)
        cr = self.cliprect.inflate( -2*(width-1), -2*(width-1))
        (pos0, pos1, accept) = clipline(pos0, pos1, cr)
        if not accept:
            return Rect( 0,0,0,0)
        return self._drawop(pygame.draw.line,
                     col,pos0,pos1,width,temp=temp)
    def lines(self,positions,col=None,width=1,temp=0,angle=0,zoom=1):
        """
        Draw an open sequence of lines through ``positions``,
        ``width`` defaults to 1, ``colour`` to white.
        If ``temp`` is true, then draw lines temporarily.
        ``angle`` specifies the angle the lines are rotated through
        ``zoom`` specifies the zoom factor
        (``angle`` and ``zoom`` operate around the arithmetic
        centroid of the lines)        

        Returns the bounding rectangle of the lines.        
        """
        col = self._colour(col)
        if angle != 0 or zoom != 1:
            positions = rotozoompositions(positions,angle,zoom)
        # use a simple algorithm; i.e. just pass out to line()
        # I think it is possible to do better by unwinding the line()
        # algorithm here, but that's going to be complex
        pairs = []
        posbeta = None
        ur = None
        first = 1
        for pos in positions:
            if posbeta!=None:
                r = self.line(posbeta,pos,col=col,width=width,temp=temp)
                if first:
                    ur = r
                    first = 0
                else:
                    ur = ur.union(r)
            posbeta = pos
        return ur
    def polygon(self,positions,col=None,width=0,temp=0,angle=0,zoom=1):
        """
        Draw a polygon with vertices at positions, width defaults to
        1 (0 for filled), colour to white.
        If temp is true, then draw polygon temporarily.
        angle specifies the angle the polygon is rotated through
        zoom specifies the zoom factor
        (angle and zoom operate around the arithmetic centroid of the points)        
        Returns the bounding rectangle of the polygon.        
        """
        col = self._colour(col)
        if len(positions) < 2:
            return Rect(0,0,0,0)
        if angle!=0 or zoom!=1:
            positions = rotozoompositions(positions,angle,zoom)
        if width != 0:
            self.lines( positions+[positions[0]], col, width,temp)
        else:
            # zero width
            positions = clippoly(positions, self.cliprect)
            if positions == []:
                return Rect(0,0,0,0)
            if len(positions) <= 2:
                return line(positions[0], positions[-1], width=width,col=col,temp=temp)
            else:
                return self._drawop(pygame.draw.polygon,col,positions,width,temp=temp)
    def rectangle(self,rect,rectb=None,col=None,width=0,temp=0,angle=0,zoom=1):
        """ draw a rectangle size rect.
        If width is zero or unspeciifed, draw a solid rectangle otherwise
        draw a rectangle of the given width
        If temp is true, then draw rectangle temporarily.
        angle specifies the angle the rectangle is rotated through
        zoom specifies the zoom factor
        (angle and zoom operate around the middle of the rectangle)        

        Returns the rectangle as a pygame rectangle object.        
        """
        col = self._colour(col)
        if type(rect) == type((1,2)):
            if type(rectb) == type( (1,2)):
                rect= Rect( (rect, (rectb[0]-rect[0], rectb[1]-rect[1])) )
            else:
                rect = Rect ( * rect )
        cliprect = self.cliprect.clip(rect)
        if cliprect != rect or angle != 0 or zoom != 1:
            return polygon( [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft],
                     width=width,angle=angle,zoom=zoom,temp=temp,col=col)
        if width == 0:
            if rect.width == 0 or rect.height == 0: return
            if not temp:
                self.background.fill(col,rect)
            self.screen.fill(col,rect)
            return self.touchedrect(rect,temp=temp)
        else:
            return self._drawop(pygame.draw.rect,
                         col,rect,width,temp=temp)
    def getkey(self, keycodes=None, block=1,dotick=1):
        """ wait for a keystroke, or return it from the buffer if it
        has already been pressed and so is buffered up.

        Returns a code for the key pressed. These codes are in pygame.locals
        (e.g. pygame.local.K_UP).

        In exceptional circumstances may return None.
        Automatically calls tick unless the argument dotick is specified as false.
        You can stop getkey from waiting if no keys are pressed by specifiying
        the argument block as false.        
        """        
        if dotick: self.tick()
        while 1:
            if block:
                ev = pygame.event.wait()
            else:
                ev = pygame.event.poll()
                if ev.type is pygame.locals.NOEVENT:
                    return

            #print 'Got event',ev
            if ev.type is pygame.locals.QUIT or ev.type is pygame.locals.KEYDOWN:
                if ev.type == pygame.locals.QUIT:
                    sys.exit(0)
                if keycodes and not ev.key in keycodes: continue
                return ev.key
    def getat(self, pos, temp=0):
        """ read the contents of a pixel on the screen at pos.

        If you want to read the contents of temporary and non-temporary drawing,
        set the keyword argument temp to true. Otherwise you see only drawing
        done by commands where temp was not set to true.

        Note that in this case temp is a flag; any true value will reveal
        drawing on all temporary layers.
        """
        if not temp:
            s=self.background
        else:
            s=self.screen
        if not self.screenrect.collidepoint(pos[0],pos[1]):
            return None
        return s.get_at(pos)
    def getarea(self, rect=None, temp=0):
        """ read the contents of an area of the screen (or background if temp
        is false) and return a pygame Surface containing the contents. This
        surface can then be passed to plotimage. The area can be specified
        as a rectangle, or else the current clipping area (by default
        the whole screen) will be read)

        Note that in this case temp is a flag; any true value will reveal
        drawing on all temporary layers.

        Note that getarea returns a copy of the pixel data; changing
        the returned surface will not update the screen.
        """
        if type(rect) == type(None) and rect == None:
            rect = self.cliprect
        if not temp:
            s=self.background
        else:
            s=self.screen
        rect = self.cliprect.clip(Rect(rect))
        dest = pygame.Surface(rect.size)
        dest.blit(s, (0,0), rect)
        return dest
    def waitforkeys(self, keycodes=None, dotick=1):
        """ wait for all the keys in keycodes to be released, and then
        wait for one of them to be pressed. Return the one that was
        pressed """
        if keycodes != None and type(keycodes) != type([]): keycodes = [keycodes]
        if dotick: self.tick()
        while keycodes != None:
            pressed = pygame.key.get_pressed()
            any = 0
            
            for k in keycodes:
                if pressed[k]: any = 1
            pygame.event.wait()
            if not any: break
        if keycodes == None:
            while 1:
                pressed = pygame.key.get_pressed()
                down = 0
                for i in pressed:
                    if i: down =1
                if down:
                    pygame.event.wait()
                else:
                    break
        while 1:
            pygame.event.wait()
            pressed = pygame.key.get_pressed()
            if keycodes: 
                for k in keycodes:
                    if pressed[k]: return k
            else:
                for i in range(len(pressed)):
                    if pressed[i]: return i
        # all keycodes are released
        return self.getkey(keycodes,block=1,dotick=dotick)
    def ispressed(self, keycode):
        """ check if the specified key is currently pressed, without blocking
        """
        import pygame.key
        return pygame.key.get_pressed()[keycode]
    def pause(self,milliseconds,rough=0):
        """ pause the program for the specified number of milliseconds.
        Unfortunately the program will still do work in the time you have
        it paused. If you don't mind if the pause may be a bit longer than
        you asked for, set rough=1. Unfortunately the exact amount longer
        is difficult to predict, and will depend on operating system and
        what other programs are running.

        Returns the number of milliseconds the pause actually took.
        """
        import pygame.time
        milliseconds = int(milliseconds)
        if rough:
            return pygame.time.wait(milliseconds)
        else:
            return pygame.time.delay(milliseconds)
    def play(self, filename):
        """ play the sound in filename immediately. Note that
        calling play() a lot of times so that may sounds are playing
        at once may overload the sound output system, causing later
        play() requests to be overloaded."""
        self._loadsound(filename).play()
    def easygamequit(self):
        """ shut down the display (don't use the easygame calls after this) """
        self.screen = None
        import pygame.display
        pygame.display.quit()
    def quit(self):
        raise SystemExit(0)
    def addsprite(self, sprite):
        """ add sprite spplied to sprite list """
        if sprite in self.sprites:
            return
        self.sprites.append(sprite)
    def delsprite(self, sprite):
        """ delete sprite supplied from sprite list """
        for i in range(len(self.sprites)):
            if self.sprites[i] == sprite:
                del self.sprites[i]
                self.delsprite(sprite)
                return
    def spritetick(self,fps=30):
        """ a routine to be called in place of cleartemp/tick once per
        animation loop, which deals with ticking and drawing sprites.
        Also enables batching. """
        self.batching = 1
        t = tick(fps)
        if t > 1.0/fps: t = 1.0/fps
        cleartemp()
        for sprite in self.sprites:
            pass
            sprite.tick(t)
##        for sprite in self.sprites:
##            sprite.draw()
        return t
    def getspritelist(self):
        """ get the list of sprites """
        return self.sprites
    def removeallsprites(self):
        """ remove all sprites """
        self.sprites = []

_degradfac = 180.0 / math.pi
class ContradictoryPosInit(Exception): pass


class Pos:
    """
    The Pos class
    =============
    
    General purpose 2D points/vectors class, with polar and
    rectilinear coordinate support. Pos objects are immutable and so
    can be hashed.

    Examples::
        >>> Pos(1,1).direction
        -45.0
        >>> Pos(0,0).distanceto( Pos(10,10) )
        14.142135623730951
        >>> Pos(1,0) * Pos(0,1)
        0.0
        >>> Pos(1,1)*3
        Pos(3.000000,3.000000)
        >>> Pos(1,0) + Pos(0.1,0.1)
        Pos(1.100000,0.100000)
        >>> 2*Pos(1,0)
        Pos(2.000000,0.000000)
    """
    def __init__(self, *argl, **kwargs):
        """
        Supply eith rectilinear coordinates (as a 2-tuple or two nameless args), or at least one of x,y,magnitude,direction

        Examples::
            >>> Pos(3,4) # the obvious constructor
            Pos(3.000000,4.000000)
            >>> Pos( [3,4] ) # but can take sequenes such as lists...
            Pos(3.000000,4.000000)
            >>> Pos( (3,4) ) # or tuples
            Pos(3.000000,4.000000)
            >>> Pos( ) # or just nothing for the origin
            Pos(0.000000,0.000000)
            >>> Pos( x=1) # or just one rectilinear component (other implicitly 0)
            Pos(1.000000,0.000000)
            >>> Pos( x=1, y=2) # or both, if you prefer typing pratice
            Pos(1.000000,2.000000)
            >>> Pos(y=2) # or, you guessed it, just the y component
            Pos(0.000000,2.000000)
            >>> Pos(magnitude=1) # asking for a unit length vector, default direction of zero
            Pos(1.000000,0.000000)
            >>> Pos(direction=45) # asking for a position at angle 45, default to unit length
            Pos(0.707107,-0.707107)
            >>> Pos(magnitude=2, direction=45) # specifying both magnitude and direction
            Pos(1.414214,-1.414214)
            >>> Pos(Pos(1,2))
            Pos(1.000000,2.000000)
        """
        if len(argl) == 0 and kwargs == {}:
            x,y = 0,0
        elif len(argl) == 2:
            x,y = argl
        elif len(argl) == 1:
            t = argl[0]
            if isinstance(t, Pos):
                x,y = t
            elif (type(t) in [type((1,2)), type([])] and len(t) == 2) or (
              type(t) == type(self) and t.__class__.__name__ == 'Pos'):
                x, y = t
            else:
                raise TypeError('a single '+repr(type(t))+' argument to Pos must be either a 2-list or 2-tuple')
        else: 
            keys = list(kwargs.keys())
            keys.sort()        
            if keys in [['magnitude'],
                        ['direction','magnitude'],
                        ['direction']]:
                magnitude = 1
                direction = 0
                if 'magnitude' in kwargs: magnitude = kwargs['magnitude']
                if 'direction' in kwargs: direction = kwargs['direction']
                anglerad = direction/_degradfac
                x = math.cos( anglerad) * magnitude
                y = -math.sin( anglerad) * magnitude
            elif keys == ['x','y']: x,y = kwargs['x'], kwargs['y']
            elif keys == ['x']: x,y  = kwargs['x'], 0.0
            elif keys == ['y']: x,y = 0.0, kwargs['y']
            else:
                raise ContradictoryPosInit(argl, kwargs)
        self.__dict__['x'] = float(x)
        self.__dict__['y'] = float(y)
    def __len__(self):
        """Pos objects have length 2 (you can use them as 2-sequences)

        Example::
            >>> len(Pos())
            2
        """
        return 2
    def __getitem__(self, k):
        """Sequence support (reading)

        Example::
            >>> p = Pos(1,2)
            >>> print p[0],p[1]
            1.0 2.0
            >>> (x,y) = p
            >>> print x, y
            1.0 2.0
        """
        if k == 0: return self.x
        if k == 1: return self.y
        if type(k) == type(1): raise IndexError(k)
        raise TypeError(k)
    def __setitem__(self, k, v):
        raise TypeError("object doesn't support item assignment")
    def __setattr__(self, k, v):
        raise TypeError("object doesn't support attribute assignment")
    def __repr__(self):
        """ Pos objects can be printed out.

        Example::
            >>> Pos()
            Pos(0.000000,0.000000)
        """
        return 'Pos(%f,%f)' % (self.x,self.y)
    def __hash__(self):
        """ Hashing. Allows Pos objects to be keys in hash tables.

        >>> t = { Pos() : 'Origin', Pos((1,0)): 'i', Pos(y=1) : 'j' }
        >>> print t[Pos(0,1)], t[Pos(0,0)]
        j Origin
        

        """
        return hash( (self.x, self.y) )
    def _promote(self, other):
        """ Internal function to promote sequences to Pos units """
        if other is None:
            return Pos()
        if not isinstance(other, Pos):
            if type(other) in [type( (1,2)), type([1,2])] and len(other) == 2:
                return Pos(other[0], other[1])
            else:
                raise TypeError("Cannot convert " + repr(other) +" into a 2-vector")
        else:
            return other
    def __add__(self, other):
        """ Normal add.
        Example::
            >>> Pos(1,2) + (1,0)
            Pos(2.000000,2.000000)
        """
        other = self._promote(other)
        return Pos(self.x+other.x, self.y+other.y)
    def __radd__(self,other):
        """ Normal add.
        Example::
        
            >>> (1,2) + Pos(3,4)
            Pos(4.000000,6.000000)
        """
        return self.__add__(other)
    def __iadd__(self, other):
        """ In-place add.
        
        Example::
            >>> a = Pos(2,3)
            >>> b = a
            >>> a += (1,2)
            >>> print a
            Pos(3.000000,5.000000)
            >>> print id(a) == id(b)
            0
        """
        other = self._promote(other)
        return Pos(self.x+other.x, self.y+other.y)
    def __sub__(self,other):
        """ Subtraction against another position

        Example::
            >>> Pos(2,1) - (1,0)
            Pos(1.000000,1.000000)
            >>> Pos(2,1) - Pos(2,2)
            Pos(0.000000,-1.000000)
        """
        other = self._promote(other)
        return Pos(self.x-other.x, self.y-other.y)
    def __rsub__(self,other):
        """ subtraction 
        """
        other = self._promote(other)
        return Pos(other.x-self.x, other.y-self.y)
    def __isub__(self, other):
        """ in place subtraction 
        """
        other = self._promote(other)
        return Pos(self.x - other.x, self.y - other.y)
    def __mul__(self,other):
        """

        Multiplication by scalars or vectors. Scalar multiplication
        scales the result, vector multiplication does cross product.

        Example::
            >>> Pos(3,4) * 2
            Pos(6.000000,8.000000)
            >>> Pos(3,4) * Pos(1,0)
            3.0
		"""
        if type(other) in [type(1), type(1.0)]:
            return Pos(self.x*other, self.y*other)
        other = self._promote(other)
        return self.x*other.x + self.y*other.y
    def __rmul__(self, other):
        """ Multiplication. 
        """
        return self.__mul__(other)
    def __imul__(self, other):
        """ in place multiplication 
        """
        if type(other) in [type(1), type(1.01)]:
            return Pos(self.x*other, self.y*other)
        other = self._promote(other)
        return self.x*other.x + self.y*other.y
    def __truediv__(self, other):
        """ true (floating point) division 
        Example::
            >>> Pos(1,2)/2
            Pos(0.500000,1.000000)
        """
        return Pos(self.x / other, self.y/other)
    def __rtruediv__(self, other):
        """ true (floating point) division 
        Example::
            >>> Pos(1,2)/2
            Pos(0.500000,1.000000)
        """
        return Pos(self.x / other, self.y/other)
    def __itruediv__(self, other):
        """ in place true (floating point) division 
        Example::
            >>> a=Pos(1,2)
            >>> a /= 2
            Pos(0.500000,1.000000)
        """
        return Pos(self.x / other, self.y/other)
    def __floordiv__(self, other):
        """ integer division
        Example::
            >>> Pos(1,2)//2
            Pos(0.000000,1.000000)
        """
        return Pos(self.x//other, self.y//other)
    def __rfloordiv__(self, other):
        """ integer division
        Example::
            >>> Pos(1,2)/2
            Pos(0.500000,1.000000)
        """
        return Pos(other//self.x, other//self.y)
    def __ifloordiv__(self, other):
        """ in place integer division
        Example::
            >>> a=Pos(1,2)
            >>> a //= 2
            Pos(0.500000,1.000000)
        """
        return Pos(self.x//other, self.y//other)
    def __neg__(self):
        """ negative (does a copy)
        Example::
            >>> -Pos(1,2)
            Pos(-1.000000,-2.000000)
        """
        return Pos(-self.x, -self.y)
    def __pos__(self):
        """ positive (does a copy)

        Example::
            >>> p = Pos(1,2)
            >>> id(p) == id(+p)
            0

        """
        return Pos(self.x, self.y)
    def __eq__(self, other):
        """self.__eq__(other) <==> self==other
        """
        # print('eq', self, other)
        other = self._promote(other)
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        """self.__ne__(other) <==> self!=other
        """
        other = self._promote(other)
        return self.x != other.x or self.y != other.y
    def __lt__(self, other):
        """self.__lt__(other) <==> self<other
        """
        other = self._promote(other)
        return (self.x,self.y) < (other.x,other.y)
    def __le__(self, other):
        """self.__le__(other) <==> self<=other
        """
        other = self._promote(other)
        return (self.x,self.y) <= (other.x,other.y)
    def __gt__(self, other):
        """self.__gt__(other) <==> self>other
        """
        other = self._promote(other)
        return (self.x,self.y) > (other.x,other.y)
    def __ge__(self, other):
        """self.__ge__(other) <==> self>=other
        """
        other = self._promote(other)
        return (self.x,self.y) >= (other.x,other.y)
    def distanceto(self, other):
        """ Calculate the L1 distance between this position and other.

        Example::
            >>> Pos(2,3).distanceto(Pos(5,6))
            4.2426406871192848
            >>> Pos(2,3).distanceto((5,6)) # you can just give a sequence if you prefer
            4.2426406871192848
        """
        other = self._promote(other)
        return (self-other).magnitude
    def mdistanceto(self, other):
        """ Calculate the L∞ (manhattan) distance between this position and other.
        
        Example::
            >>> Pos(2,3).mdistanceto((5,6))
            3
            >>> Pos().mdistanceto((5,6))
            6
        """
        other = self._promote(other)
        return max(abs(self.x-other.x), abs(self.y-other.y))
    def __getattr__(self, name):
        """
        Allow users to lookup direction and magntiude.

        Example::
            >>> Pos(1,1).direction
            -45.0
            >>> Pos(1,1).magnitude
            1.4142135623730951
        """
        if name == 'magnitude': return math.sqrt(self.x*self.x + self.y*self.y)
        if name == 'direction': return math.atan2(-self.y,self.x)*_degradfac
        raise AttributeError(name)
    def compmult(self, other):
        """ Return a new Pos, with component-wise multiplication performed.

        Example::
            >>> Pos( (1,2)) . compmult( (-1,1) )
            Pos(-1.000000,2.000000)
            >>> p = Pos( (2,3) )
            >>> print p
            Pos(2.000000,3.000000)
            >>> p.compmult( (-1, 1))
            Pos(-2.000000,3.000000)
            >>> print p
            Pos(2.000000,3.000000)
        """
        other = self._promote(other)
        return Pos(self.x * other.x, self.y * other.y)
    def setx(self, x):
        """ Return a new Pos, with the X coordinate changed

        Example::
            >>> p = Pos( (2,3) )
            >>> p.setx(4)
            Pos(4.000000,3.000000)
            >>> print p
            Pos(2.000000,3.000000)
        """
        return Pos(x, self.y)
    def sety(self, y):
        """ Return a new Pos, with the Y coordinate changed

        Example::
            >>> p = Pos( (2,3) )
            >>> p.sety(0)
            Pos(2.000000,0.000000)
            >>> print p
            Pos(2.000000,3.000000)

        """
        return Pos(self.x, y)
    def setmagnitude(self, magn):
        """ Return a new Pos, with the magnitude changed.

        Example::
            >>> p = Pos ( (1,1) )
            >>> p.setmagnitude(4)
            Pos(2.828427,2.828427)
            >>> print p
            Pos(1.000000,1.000000)
            >>> print p.magnitude
            1.41421356237

        """
        return Pos(magnitude=magn, direction=self.direction)
    def setdirection(self, direction):
        """ Return a new Pos, with the direction changed.
        
        Example::
            >>> Pos(1,0).setdirection(45)
            Pos(0.707107,-0.707107)
        """
        return Pos(magnitude=self.magnitude, direction=direction)
    def tointeger(self):
        """ Return a 2-tuple of int(x) and int(y)
        
        Example::
            >>> Pos(3.14,2.71).tointeger()
            (3,2)
        """
        return int(self.x), int(self.y)
def anglerange(t0, via, t1, steps, r):
    """Interpolate between ``t0`` and ``t1``, via ``via`` where ``t0,t1,via``
    are all angles in degrees. Do so in ``steps`` steps, or if ``steps``
    is None, use radius ``r`` to work out suitable number of steps for
    smooth look."""
    # work out how far it is to via, working forwards and backwards
    # from t0 and t1
    alphaplus = (via-t0)%360
    betaplus = (t1-via)%360
    alphaminus = (t0-via)%360
    betaminus = (via-t1)%360
    # go with the way which has the shortest distance to via
    if min(alphaplus, betaplus, alphaminus, betaminus) in [alphaminus, betaminus]:
        delta = -((t0-t1)%360)
    else:
        delta = (t1-t0)%360
    if steps is None:
        length = 2 * 3.14159 * r *  abs(delta) / 360
        steps = max(int(length // 20), 10)
    deltastep = delta/steps
    return [ t0 + (deltastep*step) for step in range(steps+1)]

def circleoriginfromthreepoints(pos0, pos1, pos2):
    # see http://mathworld.wolfram.com/Circle.html
    # code from http://groups.google.com/groups?hl=en&lr=&ie=UTF-8&threadm=4ihcu2%24hv1%40sylvia.smith.edu&rnum=4&prev=/groups%3Fhl%3Den%26lr%3D%26ie%3DISO-8859-1%26q%3Dcircle%2Bthree%2Bpoints%2Bcode%26sa%3DN%26tab%3Dwg

    A = pos1.x - pos0.x;
    B = pos1.y - pos0.y;
    C = pos2.x - pos0.x;
    D = pos2.y - pos0.y;

    E = A*(pos0.x + pos1.x) + B*(pos0.y + pos1.y)
    F = C*(pos0.x + pos2.x) + D*(pos0.y + pos2.y)

    G = 2.0*(A*(pos2.y - pos1.y)-B*(pos2.x - pos1.x))

    return Pos((D*E - B*F) / G, (A*F - C*E) / G)



####### STUFF TO USE IPYTHON

# CallQueue stuff from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/491281
class Full(Exception):pass
class Empty(Exception):pass

class CQItem:
    args=None
    kwargs=None
    done=0              # 1=return value; 2=exception
    delivered=0
    raise_exception=1
    def get_return(self,alt_return=None):
        """delivers the return value or (by default) echoes the exception of the call job
        """
        if self.done==2:
            if self.raise_exception & 1:    #by default exception is raised
                exc=self.exc
                del self.exc
                raise exc[0](exc[1]).with_traceback(exc[2])
            else:
                return alt_return
        return self.ret
    def get_exception(self):
        return self.exc
    def is_done(self):
        """returns 1, if the call return's a value; 2, if an exception was raised
        """
        return self.done
    def complete(self):
        while not self.is_done():
            time.sleep(0.05)
            
        return self.get_return()

class CallQueue:
    closed=0
    exc=None
    max_dthreads=0
    dthreads_count=0
    def __init__(self,maxsize=None,max_default_consumer_threads=0):
        self.fifo=[]            # self.fifo=Queue.Queue() not necessary, if .append() and .pop(0) Python atomic
        self.collected=[]
        self.maxsize=maxsize    # approximate guarantee, if Queue.Queue is not used
        self.max_dthreads=max_default_consumer_threads
    def call( self, func, args=(), kwargs={}, wait=0, timeout=None, raise_exception=1, alt_return=None ):
        """Puts a call into the queue and optionally waits for return.
        
        wait:  0=asynchronous call. A call queue item is returned
               1=waits for return value or exception
               callable -> waits and wait()-call's while waiting for return
        raise_exception: 1=raise in caller, 2=raise in receiver, 3=raise in both, 
                         0=silent replace with alt_return
        """
        if self.dthreads_count<self.max_dthreads:
            self.add_default_consumer_threads(n=1)
        if self.closed:
            raise Full("queue already closed")
        cqitem=CQItem()
        cqitem.func=func
        cqitem.args=args
        cqitem.kwargs=kwargs
        cqitem.wait=wait
        cqitem.raise_exception=raise_exception
        if self.maxsize and len(self.fifo)>=self.maxsize:
            raise Full("queue's maxsize exceeded")
        self.fifo.append( cqitem )
        if self.closed:
            raise Full("queue already closed")
        if wait:
            starttime = _time()
            delay=0.0005
            while not cqitem.is_done():
                if timeout:
                    remaining = starttime + timeout - _time()
                    if remaining <= 0:  #time is over and no element arrived
                        if raise_exception:
                            raise Empty("return timed out")
                        else:
                            return alt_return
                    delay = min(delay * 2, remaining, .05)
                else:
                    delay = min(delay * 2, .05)
                if isinstance(wait, collections.Callable): wait()
                _sleep(delay)       #reduce CPU usage by using a sleep
            return cqitem.get_return()
        return cqitem
    def call_and_collect(self,*args,**kwargs):
        r=self.call(*args,**kwargs)
        self.collected.append(r)
        return r
    def add_default_consumer_threads(self,n=1,maxdelay=0.016):
        import _thread, weakref
        weak_self=weakref.proxy(self)
        for i in range(n):
            self.dthreads_count+=1
            tid=_thread.start_new(_default_consumer_thread,(weak_self,maxdelay))
    def is_done(self):
        """check if call-queue and collected are flushed"""
        if self.fifo or self.collected:
            return False
        return True
    def get_next_collected(self):
        next=[]
        for cqitem in self.collected[:]:
            if not isinstance(cqitem,CQItem) or cqitem.is_done():
                next.append(cqitem)
                self.collected.remove(cqitem)
        return next

    def receive(self):
        """To be called (periodically) by target thread(s). Returns number of calls handled.
        """
        count=0
        while self.fifo:
            try:
                cqitem=self.fifo.pop(0)
            except IndexError:
                break  # multi-consumer race lost
            try:
                #print cqitem.func.__name__, cqitem.args, cqitem.kwargs
                cqitem.ret=cqitem.func(*cqitem.args,**cqitem.kwargs)
                cqitem.done=1
            except:
                if cqitem.raise_exception & 1:
                    cqitem.exc=sys.exc_info()
                cqitem.done=2
                if cqitem.raise_exception & 2:
                    raise
            count+=1
        return count
            
    def qsize(self):
        """Returns current number of unconsumed calls in the queue
        """
        return len(self.fifo)
    def close(self):
        """stops further attempts for calling and terminates default consumer threads
        """
        self.closed=1
    def close_and_receive_last(self):
        self.close()
        self.receive()
    def __del__(self):
        self.close()


class TickThread:
    """ Actuall not really a thread, just the main thread acting
    in a threading.Thread type role
    """
    def __init__(self, cq, obj):
        self.loop = True
        self.cq = cq
        self.obj = obj
        self.key_stack = []
    def run(self):
        while self.loop:
            try:                
                #sys.stderr.write('.')
                if self.cq:
                    n = self.cq.receive()
##                    if n:
##                        print 'handled',n,'commands'
                #self.obj.blit((Rect( (0,0), self.obj.getscreensize())))
                if self.obj.shutdown: return
                self.obj.tick()
                ev = pygame.event.poll()
                if ev.type is pygame.locals.QUIT:
                    pygame.quit()
                    self.cq.close()
                    return
                st = 0
                if ev.type is pygame.locals.NOEVENT:
                    st = 0.1
                if ev.type is pygame.locals.KEYDOWN:
                    self.key_stack.append(ev.key)
                self.last_tick = time.time()
                if st:
                    time.sleep(st)
            except KeyboardInterrupt:
                raise
            except:
                print('Tick thread threw:')
                traceback.print_exc()
        self.finish()
    def finish(self):
        #sys.stderr.write('TT finish function top\n')
        self.obj.closedown()
        del self.obj
        self.loop = False
        #self.cq.call( lambda x:x, [1], {}).complete()
        pygame.quit()
        #print 'Tick thread set to exit'

class ShellThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tt = None
    def run(self):
        ipshell = IPShellEmbed()
        ipshell() # this call anywhere in your program will start IPython
        #print 'IP shell finish'
        tt.loop = False

def cq_getkey():
    while True:
        try:
            return tt.key_stack.pop(0)
        except IndexError:
            pass
        sys.stderr.write('waiting for keypressess...\r')
        time.sleep(0.1)

def cq_waitforkeys():
    tt.key_stack = []
    return cg_getkey()

if __name__ == '__main__':
    import sys, os, easygame
    from IPython.Shell import IPShellEmbed
    sys.testing = 1
    cq = CallQueue()
    surf = None
    if hasattr(sys, 'pygamesurf'):
        surf = getattr(sys, 'pygamesurf')
    _obj = _ScreenModel(surf=surf)
    for cmd in dir(_ScreenModel):
        if cmd[0] != '_':
##            print 'importing',cmd
            if 0:
                code += '  sys.stderr.write("cq '+cmd+'\\n")\n'
            if cmd == 'getkey':
                code = cmd+'=cq_getkey'
            else:
                code = 'def '+cmd+'(*l, **d):\n  '
                code += '  return cq.call(_obj.'+cmd+', l, d).complete()\n'
            exec(code)
            func = eval(cmd)
            func.__doc__ = getattr(_ScreenModel, cmd).__doc__
            setattr(easygame,cmd, func)
    for c in dir(_Colour):
        g = globals()
        v = getattr(_Colour, c)
        g[c]= v
    st = ShellThread()
    st.start()
    tt = TickThread(cq, _obj)
    tt.obj = _obj
    st.tt = tt
    tt.st = st
    tt.run()
##    sys.testing = 1
##    sys.path = [os.getcwd()] + sys.path
##    import doctest, easygame
##    doctest.testmod(easygame,verbose=0) # make sure the docstrings reflect reality :-)
##    print gendoc()
else:
    if (not hasattr(sys,'testing')):
        surf = None
        if hasattr(sys, 'pygamesurf'):
            surf = getattr(sys, 'pygamesurf')
        _obj = _ScreenModel(surf=surf)
        for cmd in dir(_ScreenModel):
            if cmd[0] != '_':
                try:
                    import inspect
                    fn = getattr(_obj, cmd)
                    src = inspect.getsource(fn)
                    i = src.find(':\n')
                    assert i > 0
                    d = src[:i]
                    for s in ['self,','self']:
                        if d.find(s) != -1:
                            d = d.replace(s, '')
                    while d and d[0].isspace(): d = d[1:]
                    argspec = inspect.getfullargspec(fn.__func__)
                    args = argspec[0][1:]
                    if argspec[1]: args.append('*'+argspec[1])
                    if argspec[2]: args.append('**'+argspec[2])
                    code =d+': return _obj.'+cmd+'('+','.join(args)+')'
                    exec(code)
                    eval(cmd).__doc__ = fn.__doc__
                except:
                    print('Intercepting',cmd)
                    traceback.print_exc()
                    exec('%s=_obj.%s' % (cmd,cmd))

import sys

def _btick():
    #global count
    #printat( (100,100), count)
    #count += 1
    tick(quick=1)

sys.onidletick = _btick
