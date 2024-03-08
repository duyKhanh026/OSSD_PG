import pygame
from DTO.player import Player  # Import lớp Player từ tệp player.py

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Demo')

player1 = Player(300, 350, (255, 0, 0))
player2 = Player(800, 350, (80, 110, 199))

run = True
clock = pygame.time.Clock()
while run:
	screen.fill((0, 0, 0))
	
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
