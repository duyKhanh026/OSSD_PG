import pygame
from classes.player import Player  # Import lớp Player từ tệp player.py
from values.color import *
from values.screen import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Demo')

player1 = Player(300, 350, RED)
player2 = Player(800, 350, BLUE)

run = True
clock = pygame.time.Clock()
while run:
	
	screen.fill(WHITE)
	line_spacing = 50  # Khoảng cách giữa các đường line
	for y in range(0, SCREEN_HEIGHT, line_spacing):
		pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))
	line_spacing_vertical = 50
	for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
	    pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
	
	for player in [player1, player2]:
		player.draw(screen)

	key = pygame.key.get_pressed()
	if key[pygame.K_a]:
		player1.move(-2, 0)
	elif key[pygame.K_d]:
		player1.move(2, 0)

	if key[pygame.K_LEFT]:
		player2.move(-2, 0)
	elif key[pygame.K_RIGHT]:
		player2.move(2, 0)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()
	clock.tick(60)

pygame.quit()
