'''
Version notes
Version 1.1
differs from 1.0 as it uses the ispressed() function to constantly update position rather than waitforkeys()
Added a map, based on a text file, and collision detection (due to check fors, moving in two directions is rather slow).

Version 2.0
Adds an enemy that needs avoiding

Version 2.1
Adds corridors between rooms and vim to limit edit tool use

Version 3.0
Removes edit ability and exapnds map, texture changes

Version 3.1
The world around you is changing

Version 3.2
Removed old map text and other commented out lines
'''

from easygame import *
import random
import time

texts = open("pagedev.txt","r")
pages = texts.readlines()

setbatching(1)

screensize = [800,600]
setmode((screensize[0],screensize[1]))
plotimage(Pos(400,300),"Sprites\Logo.png",temp=1)
tick()
time.sleep(1)
printat(Pos(400,100),"Avoid everyone, take everything",fg=Colour.red,pointsize=30,temp=1)
tick()
time.sleep(1)

TILES = []

FORWARD = Pos(0,-1)
BACKWARD = Pos(0,1)
LEFT = Pos(-1,0)
RIGHT = Pos(1,0)
DIRECTIONS = [FORWARD,LEFT,BACKWARD,RIGHT]

CHECKRIGHT = Pos(19,0)
CHECKBACK = Pos(0,19)
BACKRIGHT = Pos(19,19)

GRIDSIZE = [((screensize[0] - 40) // 20),((screensize[1] - 40) // 20)] #Width // 20, Height // 20 (Grid starts at 20,20)
GRIDSIZE = [38,28]
GRIDSIZEPOS = Pos(GRIDSIZE[0] * 20, GRIDSIZE[1] * 20) + ((RIGHT + BACKWARD) * 20) #GRIDSIZEPOS is used to determine the extreme coordinates of the grid

GRIDLIST = []

for i in range(GRIDSIZE[0]):
	for j in range(GRIDSIZE[1]):
		GRIDLIST.append(Pos((20*i)+20,(20*j)+20))

class Player:

	def __init__(self,position):
		self.position = position
		self.health = 1

	def move(self,direction):
		newpos = self.position + direction
		if (newpos // 20) * 20 in TILES and ((newpos + CHECKRIGHT) // 20) * 20 in TILES and ((newpos + CHECKBACK) // 20) * 20 in TILES and ((newpos + BACKRIGHT) // 20) * 20 in TILES:
			self.position += direction

class Enemy:

	def __init__(self):
		self.position = TILES[random.randint(1,len(TILES)-1)]
		while self.position[0] in range(int(protag.position[0] - 180),int(protag.position[0] + 180)) and self.position[1] in range(int(protag.position[1] - 180),int(protag.position[1] + 180)) or self.position not in GRIDLIST:
			self.position = TILES[random.randint(1,len(TILES)-1)]
		self.direction = DIRECTIONS[random.randint(0,3)]
	def move(self,direction):
		newpos = self.position + direction
		if (newpos // 20) * 20 in TILES and ((newpos + CHECKRIGHT) // 20) * 20 in TILES and ((newpos + CHECKBACK) // 20) * 20 in TILES and ((newpos + BACKRIGHT) // 20) * 20 in TILES:
			self.position = newpos
	def direct(self):
		direction = random.randint(1,100)
		if direction == 1:
			self.move(FORWARD)
			self.direction = FORWARD
		elif direction == 2:
			self.move(BACKWARD)
			self.direction = BACKWARD
		elif direction == 3:
			self.move(LEFT)
			self.direction = LEFT
		elif direction == 4:
			self.move(RIGHT)
			self.direction = RIGHT
		else:
			self.move(self.direction)

	def findplayer(self):
		if not random.randint(0,1):
			poss = [] #Poss is short for possibilities that the monster may move to
			if protag.position[0] < self.position[0]:
				poss.append(LEFT)
			elif protag.position[0] > self.position[0]:
				poss.append(RIGHT)
			if protag.position[1] < self.position[1]:
				poss.append(FORWARD)
			elif protag.position[1] > self.position[1]:
				poss.append(BACKWARD)
			if len(poss) > 1:
				self.move(poss[random.randint(0,len(poss)-1)])
			elif len(poss) != 0:
				self.move(poss[0])
			#Killing the player
			if self.position[0] in range(int(protag.position[0]-19),int(protag.position[0]+19)):
				if self.position[1] in range(int(protag.position[1]-19),int(protag.position[1]+19)):
					protag.health = 0

class Vim():
	def __init__(self):
		self.position = TILES[random.randint(1,len(TILES)-1)]
		while self.position[0] in range(int(protag.position[0] - 180),int(protag.position[0] + 180)) and self.position[1] in range(int(protag.position[1] - 180),int(protag.position[1] + 180)) or self.position not in GRIDLIST:
			self.position = TILES[random.randint(1,len(TILES)-1)]
		self.exist = True
		self.animate = -1
		if random.randint(1,100) != 1: #"random.ran...(1,N)" N controls frequency of book spawning (1/N)
			self.book = False
		else:
			self.book = True
			books.append(len(vims)-1)
	def test(self):
		if self.position[0] in range(int(protag.position[0] - 19), int(protag.position[0] + 19)):
			if self.position[1] in range(int(protag.position[1] - 19), int(protag.position[1] + 19)):
				self.exist = False
				for i in range(2):
					monsters.append(Enemy())
				vims.append(Vim())
				if self.book == True:
					clearscreen()
					tick()
					#print(pages)
					printat(Pos(screensize[0]/2,screensize[1]/2),pages[random.randint(1,len(pages)-1)].replace("\n",""),fg = Colour.red, pointsize = 30,temp=1)
					tick()
					time.sleep(5)
					cleartemp()
					tick()
	def draw(self,amount):
		if self.book == True and amount > 0:
			plotimage(self.position, "Sprites\Book.png",temp=1)
		if self.book == False:
			if amount > 0:
				self.animate += 1
				if self.animate > 13:
					self.animate = 13
			elif amount < 0:
				self.animate -= 1
				if self.animate < -2:
					self.animate = -2
			plotimage(self.position, "Sprites\Vims\VimThing" + str(self.animate // 2) + ".png",temp=1)

for i in range(GRIDSIZE[0]):
	for j in range(GRIDSIZE[1]):
		plotimage(Pos(i*20 + 20,j*20 + 20), "Sprites\FloorThings\FloorThing5.bmp")

rooms = []
roomtiles = []

rooms.append([Pos(0,0),random.randint(3,5),random.randint(3,7)])

for i in range(rooms[0][1] + 2):
	for j in range(rooms[0][2] + 2):
		roomtiles.append(Pos(-20,-20) + Pos(i*20 + 20,j*20 + 20))

roomnum = 12 #Controls total number of rooms
roomnum -= 1 #Four rooms are already made

for i in range(10):
	roomnum -= 1
	if roomnum == 0:
		break
	room = []
	comptiles = []
	roomw = random.randint(3,5) #Controls width range of room
	roomh = random.randint(3,5) #Controls height range of room
	roomx = random.randint(1,GRIDSIZE[0]-roomw)*20
	roomy = random.randint(1,GRIDSIZE[1]-roomh)*20
	for i in range(roomw + 2):
		for j in range(roomh + 2):
			comptiles.append(Pos(roomx - 20,roomy - 20) + Pos(i*20 + 20, j*20 + 20))
	for tile in comptiles:
		if tile in roomtiles:
			roomnum += 1
			continue
	for i in range(roomw + 2):
		for j in range(roomh + 2):
			roomtiles.append(Pos(roomx - 20,roomy - 20) + Pos(i*20 + 20, j*20 + 20))
	room.append(Pos(roomx,roomy))
	room.append(roomw)
	room.append(roomh)
	rooms.append(room)
	for i in range(room[1]):
		for j in range(room[2]):
			position = Pos(((i+1) *20),((j+1) *20)) + room[0]
			if position[0] < GRIDSIZEPOS[0] and position[0] > 19:
				if position[1] < GRIDSIZEPOS[1] and position[1] > 19:
					TILES.append(position)

for room in rooms:
	for i in range(room[1]):
		for j in range(room[2]):
			position = Pos(((i+1) *20),((j+1) *20)) + room[0]
			if position[0] < GRIDSIZEPOS[0] and position[0] > 19:
				if position[1] < GRIDSIZEPOS[1] and position[1] > 19:
					TILES.append(position)

def dungeonLine(x0, y0, x1, y1):
	dx = abs(x1-x0)
	dy = abs(y1-y0) 
	if x0 < x1:
		sx = 1
	else:
		sx = -1
	if y0 < y1:
		sy = 1
	else:
		sy = -1
	err = dx-dy
	while True:
		TILES.append(Pos(x0 * 20 , y0 * 20))
		if x0 == x1 and y0 == y1:
			break
		e2 = 2*err
		if e2 > -dy:
			err = err - dy
			x0 = x0 + sx
		if x0 == x1 and y0 == y1:
			TILES.append(Pos(x0 * 20 , y0 * 20))
			break
		if e2 <  dx: 
			err = err + dx
			TILES.append(Pos(x0 * 20 , y0 * 20))
			y0 = y0 + sy

for i in range(2):
	for room in rooms:
		point = (room[0]//20 + Pos(random.randint(1,room[1]),random.randint(1,room[2])))
		roomlink = random.randint(1,len(rooms)-1)
		pointlink = (rooms[roomlink][0]//20 + Pos(random.randint(1,rooms[roomlink][1]),random.randint(1,rooms[roomlink][2])))
		dungeonLine(point[0],point[1],pointlink[0],pointlink[1])
		dungeonLine(point[0]-1,point[1]-1,pointlink[0]-1,pointlink[1]-1)

def lighting(character):
	for i in range(9):
		for j in range(9):
			string = "Sprites\FloorThings\Gradient\FloorTextureThingGradient-0" + str(i) + "-0" + str(j) + ".png"
			position = ((((character.position + Pos(10,10)) // 20) * 20)+ Pos((i*20)-80,(j*20)-80))
			if position in TILES:
				plotimage(position,string, temp = 1)

def turnonforwhat():
	clearscreen()
	for tile in TILES:
		plotimage(tile,"Sprites\FloorThings\FloorTextureThing.bmp",temp=1)
	tick()
	waitforkeys([K_RETURN])
	clearscreen()
	for i in range(GRIDSIZE[0]):
		for j in range(GRIDSIZE[1]):
			plotimage(Pos((i*20)+20,(j*20)+20),"Sprites\FloorThings\FloorThing5.bmp")
	tick()

protag = Player(Pos(20,20))
monsters = []
books = []
vims = [1,1,1]
vims = [Vim() for i in range (5)]

def rungame():
	timer = 0
	ticks = 20
	while protag.health > 0:
		if ispressed(K_w) == True:
			protag.move(FORWARD)
		elif ispressed(K_s) == True:
			protag.move(BACKWARD)
		if ispressed(K_a) == True:
			protag.move(LEFT)
		elif ispressed(K_d) == True:
			protag.move(RIGHT)
		if ispressed(K_ESCAPE) == True:
			easygamequit()
			waitforkeys()

		for monster in monsters:
			if monster.position[0] in range(int(protag.position[0] - 60),int(protag.position[0] + 60)) and monster.position[1] in range(int(protag.position[1] - 60),int(protag.position[1] + 60)):
				monster.findplayer()
			elif monster.position[0] in range(int(protag.position[0] - 90),int(protag.position[0] + 90)) and monster.position[1] in range(int(protag.position[1] - 90),int(protag.position[1] + 90)) and random.randint(0,1) == 0:
				monster.direct()

		for vim in vims:
			if vim.exist == True:
				vim.test()

		cleartemp()

		lighting(protag)
		plotimage(protag.position, "Sprites\PlayerThing.bmp", temp=1)

		for monster in monsters:
			if monster.position[0] in range(int(protag.position[0] - 90),int(protag.position[0] + 90)) and monster.position[1] in range(int(protag.position[1] - 90),int(protag.position[1] + 90)):
				plotimage(monster.position, "Sprites\EnderThing.bmp", temp=1)

		for vim in vims:
			if vim.exist == True:
				if vim.position[0] in range(int(protag.position[0] - 90),int(protag.position[0] + 90)) and vim.position[1] in range(int(protag.position[1] - 90),int(protag.position[1] + 90)):
					#plotimage(vim.position, "Sprites\VimThing.bmp", temp=1)
					vim.draw(1)
				else:
					vim.draw(-1)

		tick(ticks)
		timer += 1/ticks
	return timer

for tile in TILES:
	if tile not in GRIDLIST:
		TILES.remove(tile)

for tile in TILES:
	if tile not in GRIDLIST:
		TILES.remove(tile)

for tile in TILES:
	if tile[0] < 10 or tile[0] > screensize[0] - 10 or tile[1] < 10 or tile[1] > screensize[1] - 10:
		TILES.remove(tile)

tiletest = []
for tile in TILES:
	if tile not in tiletest:
		tiletest.append(tile)
TILES = tiletest

for tile in TILES:
	plotimage(tile, "Sprites\FloorThings\FloorThing5.bmp")

printat(Pos(400,500),"Press space to start",fg=Colour.red,pointsize=30,temp=1)
tick()
waitforkeys([K_SPACE])
timetaken = rungame()

printat((screensize[0] / 2,screensize[1] / 2), "Game over", fg=Colour.red, pointsize=30)
tick()
time.sleep(2)
clearscreen()
tick()
time.sleep(0.5)
collected = 0
for vim in vims:
	if vim.exist == False and vim.book == False:
		collected += 1
printat((screensize[0] / 2,100), "Eyes collected: " + str(collected), fg=Colour.red, pointsize=30)
tick()
time.sleep(1)
printat((screensize[0] / 2,170), "Time survived: " + str(timetaken) + " seconds", fg=Colour.red, pointsize=30)
tick()
time.sleep(1)
printat((screensize[0] / 2,240), "Press space to exit", fg=Colour.red, pointsize=30)
tick()
time.sleep(1)
plotimage(Pos(screensize[0] / 2,400),"Sprites\PlayerLose.bmp")
tick()
waitforkeys([K_SPACE])
easygamequit()
