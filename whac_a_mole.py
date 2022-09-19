import pygame
from sys import exit
from random import randint

class Hammer(pygame.sprite.Sprite):
	def __init__(self, picture_path):
		super().__init__()
		self.image_scale = 1
		hammer = pygame.image.load(picture_path).convert_alpha()
		hammer = pygame.transform.rotozoom(hammer, 0, self.image_scale)
		self.image = hammer	
		self.rect = self.image.get_rect(center = (screen_width / 2, screen_height / 2))
		self.whack = pygame.mixer.Sound('assets/Audio/hit.wav')
		self.whack.set_volume(0.01)

	def test_border(self):
		pygame.draw.rect(self.image, 'Red', [0, 0, self.rect.width, self.rect.height], 1)

	def hammer_input(self):
		global mole_amount

		self.rect.center = pygame.mouse.get_pos()

		mouse_keys = pygame.mouse.get_pressed()

		if mouse_keys[0] and pygame.sprite.spritecollide(hammer, mole_group, True):
			self.whack.play()

			mole_amount -= 1

	def update(self):
		self.hammer_input()
		#self.test_border()

class Mole(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image_scale = 1
		mole = pygame.image.load('assets/Graphics/mole.png').convert_alpha()
		self.image = pygame.transform.rotozoom(mole, 0, self.image_scale)
		self.rect = self.image.get_rect(center = (x, y))

	def test_border(self):
		pygame.draw.rect(self.image, 'Red', [0, 0, self.rect.width, self.rect.height], 1)

	def update(self):
		self.test_border()
		pass

def spawn_moles(amount):
	test = 100
	min_num_x, mine_num_y = test, test
	max_num_x, max_num_y = screen_width - test, screen_height - test
	mole_x_pos, mole_y_pos = randint(min_num_x, max_num_x), randint(mine_num_y, max_num_y)

	for mole in range(amount):
		new_mole = Mole(mole_x_pos, mole_y_pos)
		mole_group.add(new_mole)
		mole_x_pos, mole_y_pos = 0, 0
		mole_x_pos, mole_y_pos = randint(min_num_x, max_num_x), randint(mine_num_y, max_num_y)

		# check if the moles collide with each other

pygame.init()

screen_width = 1800
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Whac-A-Mole')

fps = 60
clock = pygame.time.Clock()

pygame.mouse.set_visible(True)

# Hammer
hammer = Hammer('assets/Graphics/clown_hammer.png')
hammer_group = pygame.sprite.Group()
hammer_group.add(hammer)

# Mole
mole_group = pygame.sprite.Group()
mole_amount_ = 20
mole_amount = mole_amount_

spawn_moles(mole_amount)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	screen.fill((111, 196, 169))

	# Moles
	mole_group.draw(screen)
	mole_group.update()

	# Hammer
	hammer_group.draw(screen)
	hammer_group.update()

	print(f'Mole Amount {mole_amount}')

	if mole_amount == 0:
		mole_amount = mole_amount_
		spawn_moles(mole_amount)

	pygame.display.flip()
	clock.tick(fps)