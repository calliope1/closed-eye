import random
from easygame import *

class PlaySpace:

	def __init__(self, x, y, directions, pages, fullbright=False, dvorak=False, dramatic_pauses=True, dev_controls=False, dynamic_lighting=True, view_hitboxes=False):
		self.screen_size = (x,y)
		self.grid_size = (((x - 40) // 20), ((y - 40) // 20))
		self.grid_list = [Pos((20*i)+20, (20*j)+20) for i in range(self.grid_size[0]) for j in range(self.grid_size[1])]
		self.tile_hash = [[False for i in range(self.grid_size[1])] for j in range(self.grid_size[0])]
		self.wall_hash = [[None for i in range(self.grid_size[1])] for j in range(self.grid_size[0])]
		self.wall_set = set()
		self.tile_set = set()
		self.grid_to_position = [[Pos(j*20+20,i*20+20) for i in range(self.grid_size[1])] for j in range(self.grid_size[0])]
		self.player = None
		self.monsters = []
		self.books = []
		self.vims = []
		self.DIRECTIONS = directions
		self.view_hitboxes = view_hitboxes
		self.rooms = []
		self.room_hash = [[False for i in range(self.grid_size[1])] for j in range(self.grid_size[0])]
		self.pages = pages
		self.monster_coefficient = 0
		self.monster_count = 0

		# Dev tools
		self.fullbright = fullbright
		self.dvorak = dvorak
		self.dramatic_pauses = dramatic_pauses
		self.dev_controls = True
		self.dynamic_lighting = True

	def pos_to_grid(self,pos):
		return (int((pos[0]-20)//20),int((pos[1]-20)//20))

	def add_tile_by_grid(self,pos):
		'Add a tile by grid co-ordinate'
		if 0 <= pos[0] < self.grid_size[0] and 0 <= pos[1] < self.grid_size[1]:
			self.tile_hash[pos[0]][pos[1]] = True
			self.tile_set.add(tuple(pos))

	def add_tile_by_pos(self,pos):
		'Add a tile by actual co-ordinate'
		grid_pos = self.pos_to_grid(pos)
		self.add_tile_by_grid(grid_pos)

	def list_tile_positions(self):
		return [self.grid_to_position[ij[0]][ij[1]] for ij in self.tile_set]

	def list_wall_positions(self):
		return [self.grid_to_position[ij[0]][ij[1]] for ij in self.wall_set]
		#return [self.grid_to_position[i][j] for i in range(self.grid_size[0]) for j in range(self.grid_size[1]) if self.wall_hash[i][j] != None]

	def list_room_positions(self):
		return [self.grid_to_position[i][j] for i in range(self.grid_size[0]) for j in range(self.grid_size[1]) if self.room_hash[i][j]]

	def create_vim(self, n=1):
		self.vims += [Vim(self,100) for i in range(n)]

	def create_monster(self, n=1):
		self.monsters += [Enemy(self,self.DIRECTIONS) for i in range(n)]
		self.monster_count += n
		self.monster_coefficient = 25 * self.monster_count * (2 + self.monster_count)

	def initialise_walls(self):
		for i in range(self.grid_size[0]):
			for j in range(self.grid_size[1]):
				if not self.tile_hash[i][j]:
					surroundings = [(i+a-1,j+b-1) for a in range(3) for b in range(3) if 0 <= i+a-1 < self.grid_size[0] and 0 <= j+b-1 < self.grid_size[1]]
					if any([self.tile_hash[ab[0]][ab[1]] for ab in surroundings]):
						new_wall = GamePiece(self.grid_to_position[i][j], "square")
						self.wall_hash[i][j] = new_wall
						self.wall_set.add((i,j))

	def create_room_from_grid(self,pos,width,height):
		'Creates a room with top left grid co-ordinate pos that extends right width-many and down height-many tiles'
		width = min(width, self.grid_size[0] - pos[0] + 1)
		height = min(height, self.grid_size[1] - pos[1] + 1)
		for i in range(width):
			for j in range(height):
				self.add_tile_by_grid((pos[0] + i, pos[1] + j))
				self.room_hash[pos[0] + i][pos[1] + j] = True
		self.rooms.append((pos,width,height))

class GamePiece:
	def __init__(self, position, shape):
		self.shape = shape
		self.position = position

	def detect_collision(self, other, debug=False):
		if self.shape == "circle":
			if other.shape == "circle":
				x_diff = abs(self.position[0] - other.position[0])
				y_diff = abs(self.position[1] - other.position[1])
				if debug:
					print("cc")
					print(self.position)
					print(other.position)
					print(str(x_diff) + " " + str(y_diff))
				return x_diff**2 + y_diff**2 < 400
			elif other.shape == "square":
				other_walls = {(other.position[0] + i * 20, other.position[1] + j) for i in range(2) for j in range(20)}
				other_walls.update({(other.position[0] + i, other.position[1] + j * 20) for i in range(20) for j in range(2)})
				self.create_bounding_box()
				if debug:
					print("cs")
					print(self.position)
					print(other.position)
				if [pos for pos in self.bounding_box for corner in other_walls if (pos[0] == corner[0] and pos[1] == corner[1])]:
					return True
				return False
		elif self.shape == "square":
			if other.shape == "circle":
				collapsed_position = other.position
				if other.position[0] >= self.position[0]:
					collapsed_position -= Pos(20,0)
				if other.position[1] >= self.position[1]:
					collapsed_position -= Pos(0,20)
				x_diff = abs(self.position[0] - collapsed_position[0])
				y_diff = abs(self.position[1] - collapsed_position[1])
				if debug:
					print("sc")
					print(self.position)
					print(collapsed_position)
					print(other.position)
					print(str(x_diff) + " " + str(y_diff))
				return x_diff**2 + y_diff**2 < 400
			elif other.shape == "square":
				return (self.position[0] in range(int(other.position[0]-19),int(other.position[0]+19))
						and self.position[1] in range(int(other.position[1]-19),int(other.position[1]+19)))

class MobileObject(GamePiece):
	def __init__(self, position, shape, speed=1, noclip=False):
		super().__init__(position, shape)
		self.speed = speed
		self.noclip = noclip
		self.bounding_box = None
		self.create_bounding_box()

	def create_bounding_box(self):
		if self.shape == "circle":
			self.bounding_box = [(self.position[0] + i, self.position[1] + j) for i in range(20) for j in range(20) if (i + j >= 5) and (j - i <= 14) and (i - j <= 13) and (i + j <= 32)]
		else:
			self.bounding_box = None
	
	def move(self,direction,ps,debug=False):
		newpos = self.position + direction * self.speed
		if self.noclip:
			self.position = newpos
			return True
		else:
			oldpos = self.position
			self.position = newpos
			grid_pos = ps.pos_to_grid(newpos)
			possible_walls = [ps.wall_hash[grid_pos[0] + i][grid_pos[1] + j] for i in range(2) for j in range(2) if ps.wall_hash[grid_pos[0] + i][grid_pos[1] + j] != None]
			if any([self.detect_collision(wall,debug) for wall in possible_walls]):
				self.position = oldpos
				return False
			return True
			# grid_pos = ps.pos_to_grid(newpos)
			# x_mis = newpos[0] % 20
			# y_mis = newpos[0] % 20
			# x_ind = int(min(x_mis,1))
			# y_ind = int(min(y_mis,1))
			# if debug:
			# 	print(newpos)
			# 	oldpos = self.position
			# 	self.position = newpos
			# 	print([self.detect_collision(ps.wall_hash[grid_pos[0]+i][grid_pos[1] + j],True) for i in range(2) for j in range(2) if ps.wall_hash[grid_pos[0]+i][grid_pos[1]+j] != None])
			# if self.shape == "circle":
			# 	oldpos = self.position
			# 	self.position = newpos
			# 	if any([self.detect_collision(ps.wall_hash[grid_pos[0]+i][grid_pos[1] + j]) for i in range(2) for j in range(2) if ps.wall_hash[grid_pos[0]+i][grid_pos[1]+j] != None]):
			# 		self.position = oldpos
			# 		return False
			# 	return True
			# else:
			# 	if newpos[0] > ps.grid_size[0] * 20 or newpos[0] < 20 or newpos[1] > ps.grid_size[1] * 20 or newpos[1] < 20:
			# 		return False
			# 	elif all([ps.tile_hash[grid_pos[0] + i][grid_pos[1] + j] for i in range(1+x_ind) for j in range(1+y_ind)]):
			# 		self.position = newpos
			# 		return True
			# 	return False

class Player(MobileObject):

	def __init__(self,position,speed=1,noclip=False):
		super().__init__(position, "circle", speed, noclip)
		self.health = 1

class Enemy(MobileObject):

	def __init__(self,ps,directions,position=Pos(0,0),speed=1,noclip=False):
		super().__init__(position, "circle", speed, noclip)
		self.position = self.random_starting_location(ps)
		self.DIRECTIONS = directions
		self.FORWARD = self.DIRECTIONS[0]
		self.LEFT = self.DIRECTIONS[1]
		self.BACKWARD = self.DIRECTIONS[2]
		self.RIGHT = self.DIRECTIONS[3]
		self.direction = random.choice(self.DIRECTIONS)
		self.blocked = False

	def random_starting_location(self, ps):
		tile_set = ps.tile_set
		protag = ps.player
		grid_position = random.choice(tuple(tile_set))
		try_position = ps.grid_to_position[grid_position[0]][grid_position[1]]
		attempts = 0
		while attempts < 20 and (try_position[0] in range(int(protag.position[0] - 180),int(protag.position[0] + 180))
							and try_position[1] in range(int(protag.position[1] - 180),int(protag.position[1] + 180))
						   or try_position not in ps.grid_list):
			grid_position = random.choice(tuple(tile_set))
			try_position = ps.grid_to_position[grid_position[0]][grid_position[1]]
			attempts += 1
			if attempts == 20:
				grid_position = random.choice(tuple(tile_set))
				try_position = ps.grid_to_position[grid_position[0]][grid_position[1]]
		return try_position

	def direct(self,ps):
		if self.blocked:
			self.direction = random.choice(self.DIRECTIONS)
			self.blocked = False
		i = random.randint(0,19)
		if i < len(self.DIRECTIONS):
			if self.move(self.DIRECTIONS[i],ps):
				self.blocked = False
				self.direction = self.DIRECTIONS[i]
			else:
				self.blocked = True
		else:
			self.move(self.direction,ps)

	def findplayer(self,protag,ps):
		if not random.randint(0,1):
			poss = [] #Poss is short for possibilities that the monster may move to
			if protag.position[0] < self.position[0]:
				poss.append(self.LEFT)
			elif protag.position[0] > self.position[0]:
				poss.append(self.RIGHT)
			if protag.position[1] < self.position[1]:
				poss.append(self.FORWARD)
			elif protag.position[1] > self.position[1]:
				poss.append(self.BACKWARD)
			if poss:
				self.move(random.choice(poss),ps)
			#Killing the player
			if self.detect_collision(protag):
				protag.health = 0
			#if self.position[0] in range(int(protag.position[0]-19),int(protag.position[0]+19)):
			#	if self.position[1] in range(int(protag.position[1]-19),int(protag.position[1]+19)):
			#		protag.health = 0

class Vim(GamePiece):

	def __init__(self,ps,book_probability=100):
		super().__init__((-20,-20),"circle")
		self.exist = True
		self.book = not random.randint(0,book_probability-1)
		self.animation_frame = -4
		self.random_position(ps)

	def random_position(self,ps):
		tile_set = ps.tile_set
		protag = ps.player
		grid_position = random.choice(tuple(tile_set))
		self.position = ps.grid_to_position[grid_position[0]][grid_position[1]]
		attempts = 0
		while attempts < 20 and (self.position[0] in range(int(protag.position[0] - 180),int(protag.position[0] + 180))
							and self.position[1] in range(int(protag.position[1] - 180),int(protag.position[1] + 180))
						   or self.position not in ps.grid_list):
			grid_position = random.choice(tuple(tile_set))
			self.position = ps.grid_to_position[grid_position[0]][grid_position[1]]
			attempts += 1
			if attempts == 20:
				grid_position = random.choice(tuple(tile_set))
				self.position = ps.grid_to_position[grid_position[0]][grid_position[1]]

	def animate(self,protag):
		if self.exist:
			if self.book:
				if (self.position[0] - protag.position[0]) ** 2 + (self.position[1] - protag.position[1]) ** 2 < 6400:
					plotimage(self.position, "Sprites/Book.png", temp=1)
			else:
				if (self.position[0] - protag.position[0]) ** 2 + (self.position[1] - protag.position[1]) ** 2 > 8100:
					self.animation_frame = max(-4, self.animation_frame - 1)
				else:
					self.animation_frame = min(26, self.animation_frame + 2) # The eye opening is faster
				plotimage(self.position, "Sprites/Vims/Vim" + str(self.animation_frame // 4) + ".png",temp=1)

	def collide(self,protag,ps,dramatic_sleep):
		if self.exist:
			if self.detect_collision(protag):
				self.exist = False
				ps.create_monster(2)
				ps.create_vim()
				if self.book:
					clearscreen()
					tick()
					#print(pages)
					printat(Pos(ps.screen_size[0]//2,ps.screen_size[1]//2),random.choice(ps.pages).replace("\n",""),fg = Colour.red, pointsize = 30,temp=1)
					tick()
					dramatic_sleep(5)
					cleartemp()
					tick()
				return True
		return False

class VimTwo:
	def __init__(self,ps):
		tile_set = ps.tile_set
		protag = ps.player
		grid_position = random.choice(tuple(tile_set))
		self.position = ps.grid_to_position[grid_position[0]][grid_position[1]]
		attempts = 0
		while attempts < 20 and (self.position[0] in range(int(protag.position[0] - 180),int(protag.position[0] + 180))
							and self.position[1] in range(int(protag.position[1] - 180),int(protag.position[1] + 180))
						   or self.position not in ps.grid_list):
			grid_position = random.choice(tuple(tile_set))
			self.position = ps.grid_to_position[grid_position[0]][grid_position[1]]
			attempts += 1
			if attempts == 20:
				grid_position = random.choice(tuple(tile_set))
				self.position = ps.grid_to_position[grid_position[0]][grid_position[1]]
		self.exist = True
		self.animate = -1
		if random.randint(1,100) != 1:
			self.book = False
		else:
			self.book = True
			ps.books.append(len(ps.vims)-1)
	def test(self,protag,ps):
		if self.position[0] in range(int(protag.position[0] - 19), int(protag.position[0] + 19)):
			if self.position[1] in range(int(protag.position[1] - 19), int(protag.position[1] + 19)):
				self.exist = False
				for i in range(2):
					ps.create_monster()
				ps.create_vim()
				if self.book:
					clearscreen()
					tick()
					print(pages)
					printat(Pos(screensize[0]/2,screensize[1]/2),pages[random.randint(1,len(pages)-1)].replace("\n",""),fg = Colour.red, pointsize = 30,temp=1)
					tick()
					dramatic_sleep(5)
					cleartemp()
					tick()
	def draw(self,amount):
		if self.book and amount > 0:
			plotimage(self.position, "Sprites/Book.png",temp=1)
		if self.book == False:
			if amount > 0:
				self.animate = min(26, self.animate + 2)
			elif amount < 0:
				self.animate = max(-4, self.animate - 1)
			plotimage(self.position, "Sprites/Vims/Vim" + str(self.animate // 4) + ".png",temp=1)