import sys, os, pygame, random
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

screen_x = 512
screen_y = 512
tile_x = 24
tile_y = 24
screen_x += tile_x - screen_x % tile_x
screen_y += tile_y - screen_y % tile_y

map_x = screen_x / tile_x
map_y = screen_y / tile_y

default_fps = 12

trail = pygame.Surface((tile_x,tile_y))
trail.fill((5,5,5))

class pos(object):
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
	def __getitem__(self, index):
		if   index == 0: return self.x
		elif index == 1: return self.y
	def __setitem__(self, index, value):
		if   index == 0: self.x = value
		elif index == 1: self.y = value
	def __add__(self, other):
		return pos(self[0]+other[0], self[1]+other[1])
	def __mod__(self, other):
		return pos(self[0]%other[0], self[1]%other[1])
	def __mul__(self, other):
		return pos(self[0]*other[0], self[1]*other[1])
	def __div__(self, other):
		return pos(self[0]/other[0], self[1]/other[1])
	def __sub__(self, other):
		return pos(self[0]-other[0], self[1]-other[1])
	def __str__(self):
		return "pos(%i,%i)" % (self[0], self[1])
	def __getslice__(self, start, end):
		return pos(self.x, self.y) #Fu*k you :3
	def __len__(self):
		return 2
	def list(self):
		return [self.x,self.y]
	def tuple(self):
		return (self.x,self.y)
	def int(self):
		return [int(self.x), int(self.y)]
	def swap(self):
		return pos(self.y, self.x)
	def move(self, vector):
		self.x+=vector[0]
		self.y+=vector[1]
		if   self.x > map_x-1: self.x-=map_x
		elif self.x < 0:       self.x+=map_x
		if   self.y > map_y-1: self.y-=map_y
		elif self.y < 0:       self.y+=map_y
		return self
	def __eq__(self, other):
		if (self.x==other.x) and (self.y==other.y): return 1
		return 0

class SnakeSegment(object):
	def __init__(self, x, y, direction):
		self.position = pos(x,y)
		self.direction = direction
	def copy(self): return SnakeSegment(self.position[0], self.position[1], self.direction)
	def __eq__(self, other):
		return (self.position == other.position)

class Snake(object):
	color1 = (255,255,255)
	color2 = (200,200,200)
	ghost_color = (35,35,35)
	start_pos = pos(0,0)
	start_dir = pos(1,0)
	def __init__(self):
		self.spawn()

	def spawn(self):
		self.dir = self.start_dir[:]
		self.body = [SnakeSegment(self.start_pos[0],self.start_pos[1], self.start_dir)]
		self.length = 5
		self.ghost = 0
		self.score = 0

	def simulate(self, bg):
		self.body+=[SnakeSegment( self.body[-1].position[0] , self.body[-1].position[1], self.dir ) ]
		#self.body[-1].position = self.body[-1].position.move(self.dir)
		self.body[-1].position.move(self.dir)
		while len(self.body) > self.length:
			bg.blit(trail, (self.body[0].position*(tile_x,tile_y)).list(), None, BLEND_RGBA_SUB )
			del self.body[0]
		#self.check_bounds()
		self.check_collision(self)
		if self.ghost and self.score >= 5:
			self.score -= 5
		if self.ghost == -1: self.ghost = 1

	def check_collision(self, snake):
		if snake.ghost == 1: return None
		bound = max(-2,-len(snake.body))
		if self==snake: bound = -1
		for i in range(0, len(snake.body)-1):
			for x in range(bound, 0):
				if self.body[x] == snake.body[i]:
					if self.ghost:
						if self.score>=20:
							self.score-=20
					else:
						self.die()

	def set_dir(self, x, y):
		p = self.body[-1].position[:]
		p.move((x,y))
		for i in self.body:
			if p==i.position: return None
		self.dir = pos(x, y)

	def die(self):
		self.length = max (5, int(self.length*2/3))
		self.ghost = -1

	def get_color(self, index):
		if self.ghost: color = self.ghost_color
		elif index&2:  color = self.color1
		else:          color = self.color2
		return color

	def draw_segment(self, index, surface):
		pos = self.body[index].position[:]
		pos*=(tile_x, tile_y)
		rect =  pygame.Rect(pos.list(), (tile_x, tile_y))
		pygame.draw.rect(surface, self.get_color(index), rect)

	def draw_head(self, index, surface):
		p1 = self.body[index].position[:]
		dir = self.body[index].direction
		p1*=(tile_x, tile_y)
		p1-= (dir * (tile_x, tile_y))
		if dir[0]==1 or dir[1]==1:
			p1+=(tile_x, tile_y)
		p2 = p1[:]
		p2-=dir.swap() * (tile_x, tile_y)
		p3 = pos()
		p3 = (p1+p2)/pos(2,2) + dir * (tile_x, tile_y)
		points = [ p1.list(), p2.list(), p3.list()]
		pygame.draw.polygon(surface, self.get_color(index), points, 0)

	def render(self, surface):
		for i in range(0,len(self.body)):
			if i==len(self.body)-1:
				self.draw_head(i, surface)
			else:
				self.draw_segment(i, surface)

class Snake1(Snake):
	color1 = (45,120,45)
	color2 = (50,140,50)
	ghost_color = (40,65,45)
	start_pos = pos(0,3)
	start_dir = pos(1,0)

class Snake2(Snake):
	color1 = (140,45,95)
	color2 = (120,35,80)
	ghost_color = (65,40,45)
	start_pos = pos(0,14)
	start_dir = pos(1,0)

class Cherry:
	color = [
		( 80,190, 20),
		(220, 20, 20),
		(210,210, 50)
	]
	def __init__(self):
		self.spawn()
	def render(self, surface):
		pos = self.pos[:]
		pos*=(tile_x, tile_y)
		pos+=(tile_x/2, tile_y/2)
		color = self.color[self.power-1]
		pygame.draw.circle(surface, color, pos.list(), 3+2*self.power, 0)
	def check_collision(self, snake):
		if snake.body[-1].position == self.pos:
			if not snake.ghost: snake.score += 250 * self.power
			snake.ghost = 0
			snake.length += 1
			if self.power == 3: snake.length += 1
			self.spawn()
	def spawn(self):
		r = random.randint(0,9)
		if   r == 0: self.power = 3
		elif r < 4:  self.power = 2
		else:        self.power = 1
		self.pos = pos(random.randint(0,screen_x/tile_x-1), random.randint(0,screen_y/tile_y-1))

class GAME:
	def __init__(self):
		pygame.init()
		pygame.mouse.set_visible(0)
		self.run=1
		self.clock = pygame.time.Clock()
		self.screen=pygame.display.set_mode((screen_x,screen_y))
		pygame.display.set_caption("")

		self.backbuff = pygame.Surface((screen_x,screen_y), 0, 32)
		self.backbuff.convert_alpha()
		self.backbuff.fill((0,0,0,0))

		self.background = pygame.Surface((screen_x,screen_y), 0, 32)
		self.background.convert_alpha()
		self.background.fill((10,10,10))

		self.start()
	def start(self):
		self.snake1 = Snake1()
		self.snake2 = Snake2()
		self.cherry = Cherry()

		iterations = 2
		for bg_scale in range(1,iterations+1):
			print( bg_scale)
			for x in range(map_x*bg_scale):
				for y in range(map_y*bg_scale):
					v = random.randint(25,40)
					color = (v,v-3,v-2)

					position = pygame.Rect(x*tile_x/bg_scale, y*tile_y/bg_scale, tile_x, tile_y)
					if bg_scale ==1:
						pygame.draw.rect(self.background, color, position)
					else:
						pygame.draw.rect(self.background, color, position, BLEND_RGBA_ADD)

		self.fps = default_fps
		self.pause = 0
	def main(self):
		while(self.run):
			self.clock.tick(self.fps)
			self.checkEvents()
			if not self.pause:
				self.snake1.simulate(self.background)
				self.snake1.check_collision(self.snake2)

				self.snake2.simulate(self.background)
				self.snake2.check_collision(self.snake1)

				self.cherry.check_collision(self.snake1)
				self.cherry.check_collision(self.snake2)
			self.render()
	def render(self):

		self.backbuff.blit(self.background, (0,0))
		self.snake1.render(self.backbuff)
		self.snake2.render(self.backbuff)
		self.cherry.render(self.backbuff)

		font = pygame.font.Font(None, 36)
		text = font.render("%i" % self.snake1.score, 1, self.snake1.color1)
		textpos = text.get_rect()
		self.backbuff.blit(text, textpos)

		font = pygame.font.Font(None, 36)
		text = font.render("%i" % self.snake2.score, 1, self.snake2.color1)
		textpos = text.get_rect(right = screen_x)
		self.backbuff.blit(text, textpos)
		self.screen.blit(self.backbuff,  (0,0))
		pygame.display.flip()
	def checkEvents(self):
		for event in pygame.event.get():
			if event.type == QUIT: sys.exit()
			elif event.type == KEYDOWN:
				if   event.key == 119: #snake1
					self.snake1.set_dir(0, -1)
				elif event.key == 115:
					self.snake1.set_dir(0,  1)
				elif event.key == 97:
					self.snake1.set_dir(-1, 0)
				elif event.key == 100:
					self.snake1.set_dir(1, 0)
				elif event.key == 273: #snake2
					self.snake2.set_dir(0, -1)
				elif event.key == 274:
					self.snake2.set_dir(0,  1)
				elif event.key == 276:
					self.snake2.set_dir(-1, 0)
				elif event.key == 275:
					self.snake2.set_dir(1, 0)
				elif event.key in range(49,58):
					self.fps = (event.key-48)*3
				elif event.key == 114:
					self.start()
				elif event.key == 27:
					sys.exit()
				elif event.key == 112:
					self.pause^=1
				else: print( event.key)
			elif event.type == MOUSEBUTTONDOWN:
				continue
			elif event.type == MOUSEBUTTONUP:
				continue

if __name__ == '__main__':
	game=GAME()
	game.main()