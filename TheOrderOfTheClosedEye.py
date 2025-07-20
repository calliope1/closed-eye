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

Version 4.0 (in progress)
Remaster:
	Rename and rearrange files
	Added some dev commands for debugging
	Dynamic lighting, which required editing the easygame code
	Modified easygame to always plot top left unless otherwise asked
	Modified hitboxes to accommodate round sprites
	Cleaned up and clarified room generation
'''

from easygame import *
import random
import time
from classes import *

# Dev tools
FULLBRIGHT = True # Default False
DVORAK = False # Default False
player_speed = 4 # Default 1. Hiher is faster. You will probably get stuck in a wall if this is more than 2 unless you enable NOCLIP.
DRAMATIC_PAUSES = False # Default True
DEV_CONTROLS = True # Default False
NOCLIP = True # Default False
DYNAMIC_LIGHTING = False # Default True
VIEW_HITBOXES = True # Default False

RESET_DEV_CONTROLS = True # Default True. Undoes all the previous settings
if RESET_DEV_CONTROLS:
	FULLBRIGHT = False
	player_speed = 1
	DRAMATIC_PAUSES = True
	DEV_CONTROLS = False
	NOCLIP = False
	DYNAMIC_LIGHTING = True
	VIEW_HITBOXES = False

def dramatic_sleep(seconds):
	if DRAMATIC_PAUSES:
		time.sleep(seconds)

setbatching(1)

screensize = [800,600]
setmode((screensize[0],screensize[1]))
GRIDSIZE = [((screensize[0] - 40) // 20),((screensize[1] - 40) // 20)] #Width // 20, Height // 20 (Grid starts at 20,20, giving the screen a 20-width border)

# This acts as a loading screen while we load any more content

plotimage(Pos(screensize[0]//2,screensize[1]//2),"Sprites/Logo.bmp",temp=1,topleft=0)
tick()
dramatic_sleep(1)
printat(Pos(screensize[0]//2,100),"Avoid everyone, take everything",fg=Colour.red,pointsize=30,temp=1)
tick()
dramatic_sleep(1)

def sloppy_weighted_random_index(w_list):
	return weighted_random_index([max(i,0) for i in w_list])

def weighted_random_index(w_list):
	s = sum(w_list)
	if s <= 0 or any([k < 0 for k in w_list]):
		raise ValueError("Weighted list must have positive mass and no negative elements")
	sum_list = [sum(w_list[i:]) for i in range(len(w_list))]
	r = random.randint(1,s)
	for i in range(len(w_list)):
		if sum_list[-1 * (i + 1)] >= r:
			return i
	raise TypeError(f"For some reason the weighted random index algorithm failed.\nInput: {w_list}\nsum: {s}\nsum_list: {sum_list}\nrandom element: {r}.")

def dungeonLine(ps, x0y0, x1y1, start_adjust=(0,0), target_adjust=(0,0)):
	x0 = x0y0[0] + start_adjust[0]
	y0 = x0y0[1] + start_adjust[1]
	x1 = x1y1[0] + target_adjust[0]
	y1 = x1y1[1] + target_adjust[1]
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
		ps.add_tile_by_pos((x0 * 20, y0 * 20))

		if x0 == x1 and y0 == y1:
			break
		e2 = 2*err
		if e2 > -dy:
			err = err - dy
			x0 = x0 + sx
		if x0 == x1 and y0 == y1:
			ps.add_tile_by_pos((x0 * 20, y0 * 20))

			break
		if e2 <  dx: 
			err = err + dx
			ps.add_tile_by_pos((x0 * 20, y0 * 20))
			y0 = y0 + sy

def lighting(character,ps):
	if ps.fullbright:
		for pos in ps.list_tile_positions():
			plotimage(pos,"Sprites/Floor/FloorTexture.bmp",temp=1)
			#plotimage(Pos(pos[0]-1,pos[1]-1),"Sprites/Floor/FloorTexture21.bmp",temp=1)

	else:
		for pos in ps.list_tile_positions():
			x_diff = abs(pos[0] - (character.position[0]))
			y_diff = abs(pos[1] - (character.position[1]))
			if x_diff**2 + y_diff**2 <= 6400:
				plotimage(pos,"Sprites/Floor/FloorTexture.bmp",temp=1)
				#plotimage(Pos(pos[0]-1,pos[1]-1),"Sprites/Floor/FloorTexture21.bmp",temp=1)

		if DYNAMIC_LIGHTING:
			light = pygame.image.load("Sprites/lighting_test.png")
			grey_surface = pygame.surface.Surface((screensize[0],screensize[1]))
			grey_surface.fill(pygame.color.Color("lightgray"))
			grey_surface.blit(light,character.position-Pos(65,65)) # This isn't top left, so it needs to be slightly off-center
			screen = get_screen()
			screen.blit(grey_surface, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
			pygame.display.flip()
	
	if ps.view_hitboxes:
		for pos in ps.list_wall_positions():
			#plotimage(pos,"Sprites/wall.png")
			continue
		for pos in protag.bounding_box:
			plotimage(pos-Pos(1,1),"Sprites/dot.png",temp=1)
		for pos in ps.list_room_positions():
			plotimage(pos,"Sprites/Floor/room.bmp")

def direction_key(direction,dvorak):
	if direction == "FORWARD":
		return (dvorak and ispressed(K_COMMA)) or (not dvorak and ispressed(K_w))
	elif direction == "BACKWARD":
		return (dvorak and ispressed(K_o)) or (not dvorak and ispressed(K_s))
	elif direction == "LEFT":
		return ispressed(K_a)
	elif direction == "RIGHT":
		return (dvorak and ispressed(K_e)) or (not dvorak and ispressed(K_d))

def rungame(play_space):
	timer = 0
	ticks = 20
	while protag.health > 0:
		if direction_key("FORWARD", DVORAK):
			protag.move(FORWARD,play_space)
		elif direction_key("BACKWARD", DVORAK):
			protag.move(BACKWARD,play_space)
		if direction_key("LEFT", DVORAK):
			protag.move(LEFT,play_space)
		elif direction_key("RIGHT", DVORAK):
			protag.move(RIGHT,play_space)
		if ispressed(K_ESCAPE):
			easygamequit()
			waitforkeys()
		if DEV_CONTROLS:
			if ispressed(K_k):
				protag.health = 0
			if ispressed(K_r):
				protag.fullbright = not protag.fullbright
			if ispressed(K_n):
				protag.noclip = not protag.noclip
				print(protag.noclip)
			if ispressed(K_b):
				protag.move(Pos(0,0),play_space,True)
			if ispressed(K_p):
				print(protag.position)
				print(protag.bounding_box)

		for monster in play_space.monsters:
			augmented_protag_distance = (monster.position[0] - protag.position[0]) ** 2 + (monster.position[1] - protag.position[1]) ** 2 - play_space.monster_coefficient
			# At 2 monsters (inital), "vision" is 60 pixels, and this goes up by 10 for every new pair of monsters
			if augmented_protag_distance < 3025:
				monster.findplayer(protag,play_space)
			# Activation radius for semi-random movement, starts at 90 and goes up by 10 for every new pair
			elif augmented_protag_distance < 7225 and random.randint(0,1):
				monster.direct(play_space)

		if all([not vim.exist for vim in play_space.vims]): # this should never occur in normal gameplay
			play_space.create_vim()

		cleartemp()

		lighting(protag,play_space)
		#plotimage(Pos(0,0),"Sprites/Player.bmp") # debug
		plotimage(protag.position, "Sprites/Player.bmp", temp=1)

		for monster in play_space.monsters:
			if FULLBRIGHT:
				plotimage(monster.position, "Sprites/Enemy.bmp", temp=1)
			elif monster.position[0] in range(int(protag.position[0] - 90),int(protag.position[0] + 90)) and monster.position[1] in range(int(protag.position[1] - 90),int(protag.position[1] + 90)):
				plotimage(monster.position, "Sprites/Enemy.bmp", temp=1)

		for vim in play_space.vims:
			if vim.exist:
				vim.animate(protag)
				vim.collide(protag,play_space,dramatic_sleep)

		tick(ticks)
		timer += 1/ticks
	return timer

##################################
### ACTUAL RUNNING OF THE GAME ###
##################################

FORWARD = Pos(0,-1)
BACKWARD = Pos(0,1)
LEFT = Pos(-1,0)
RIGHT = Pos(1,0)
DIRECTIONS = [FORWARD,LEFT,BACKWARD,RIGHT]

with open("Resources/book.txt","r") as texts:
	pages = texts.readlines()

play_space = PlaySpace(screensize[0],screensize[1],DIRECTIONS,pages,FULLBRIGHT,DVORAK,DRAMATIC_PAUSES,DEV_CONTROLS,DYNAMIC_LIGHTING,VIEW_HITBOXES)

width_weights = [4 for i in range(play_space.grid_size[0])]
height_weights = [4 for i in range(play_space.grid_size[1])]

for i in [0,1]:
	for j in [0,1]:
		# Half the rooms are 'taller', half are 'wider' (though most are square-ish)
		orientation = random.randint(0,1)
		w = random.randint(3, 5 + 2 * orientation)
		h = random.randint(3, 7 - 2 * orientation)
		corner = ((play_space.grid_size[0] - w) * i, (play_space.grid_size[1] - h) * j)
		play_space.create_room_from_grid(corner,w,h)
		for a in range(w):
			width_weights[corner[0] + a] -= 1
		for b in range(h):
			width_weights[corner[1] + b] -= 1

roomnum = 10 #Controls total number of rooms
roomnum -= len(play_space.rooms) #Four rooms are already made

for i in range(min(10,roomnum)):
	w = random.randint(3,5)
	h = random.randint(3,5)
	x = sloppy_weighted_random_index(width_weights[:1-w])
	y = sloppy_weighted_random_index(height_weights[:1-h])
	play_space.create_room_from_grid((x,y),w,h)
	for a in range(w):
		width_weights[x + a] -= 1
	for b in range(h):
		height_weights[y + b] -= 1

# For each room, draw a line between a random point in that room and a random point in another (possibly identical) room
# Twice
for i in range(2):
	for room in play_space.rooms:
		start = (room[0][0] + random.randint(2, room[1] - 1) - 1, room[0][1] + random.randint(2, room[2] - 1) - 1)
		room_link = random.choice(play_space.rooms)
		target = (room_link[0][0] + random.randint(1, room_link[1]) - 1, room_link[0][1] + random.randint(1, room_link[2]) - 1)
		dungeonLine(play_space,start,target)
		if random.randint(0,1): # Sometimes the line is thicker
			dungeonLine(play_space,start,target,(-1,-1),(-1,-1))

protag = Player(Pos(20,20),player_speed,NOCLIP)
play_space.player = protag
play_space.create_vim(4)
#play_space.create_monster()

play_space.initialise_walls()

printat(Pos(screensize[0]//2,screensize[1] - 100),"Press space to start",fg=Colour.red,pointsize=30,temp=1)
tick()
waitforkeys([K_SPACE])
timetaken = rungame(play_space)

printat((screensize[0] / 2,screensize[1] / 2), "Game over", fg=Colour.red, pointsize=30)
tick()
dramatic_sleep(2)
clearscreen()
tick()
dramatic_sleep(0.5)
collected = 0
for vim in play_space.vims:
	if not vim.exist and not vim.book:
		collected += 1
printat((screensize[0] // 2, screensize[1] // 2 - 200), f"Eyes collected: {str(collected)}", fg=Colour.red, pointsize=30)
tick()
dramatic_sleep(1)
printat((screensize[0] // 2, screensize[1] // 2 - 130), f"Time survived: {str(round(timetaken,2))} seconds", fg=Colour.red, pointsize=30)
tick()
dramatic_sleep(1)
printat((screensize[0] / 2, screensize[1] // 2 - 60), "Press space to exit", fg=Colour.red, pointsize=30)
tick()
dramatic_sleep(1)
plotimage(Pos(screensize[0] // 2, screensize[1] // 2 + 100),"Sprites/PlayerLose.bmp",topleft=0)
tick()
waitforkeys([K_SPACE])
easygamequit()