

import pygame
pygame.init()

win = pygame.display.set_mode((500,480))
pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('assets/stickman_running1.png'), pygame.image.load('assets/stickman_running2.png'), pygame.image.load('assets/stickman_running3.png'), pygame.image.load('assets/stickman_running4.png'), pygame.image.load('assets/stickman_running5.png')]

char = pygame.image.load('assets/stickman_running1.png')

x = 50
y = 200
width = 40
height = 60
vel = 5

clock = pygame.time.Clock()

isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0

def redrawGameWindow():
	global walkCount
	
	win.fill((255, 255, 255))
	if walkCount + 1 >= 15:
		walkCount = 0
		
	if right:
		win.blit(walkRight[walkCount//3], (x,y))
		walkCount += 1
	else:
		win.blit(char, (x, y))
		walkCount = 0
		
	pygame.display.update() 
	


run = True

while run:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_LEFT] and x > vel: 
		x -= vel
		left = True
		right = False

	elif keys[pygame.K_RIGHT] and x < 500 - vel - width:  
		x += vel
		left = False
		right = True
		
	else: 
		left = False
		right = False
		walkCount = 0
		
	if not(isJump):
		if keys[pygame.K_SPACE]:
			isJump = True
			left = False
			right = False
			walkCount = 0
	else:
		if jumpCount >= -10:
			y -= (jumpCount * abs(jumpCount)) * 0.5
			jumpCount -= 1
		else: 
			jumpCount = 10
			isJump = False

	redrawGameWindow() 
	
	
pygame.quit()