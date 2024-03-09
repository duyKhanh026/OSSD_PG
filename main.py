import pygame as py
from classes.player import Player
from values.color import *
from values.screen import *


def check_collision(p1, p2):
	return p1.rect.colliderect(p2.rect)

def handle_attack(attacker, victim):
	if check_collision(attacker, victim):
		victim.health -= 1
def draw_punch_effect(screen, player):
	if player.punched:
		if player.side == 'L':
			py.draw.rect(screen, (255, 150, 0), py.Rect(player.rect.x, player.rect.y, player.SQUARE_SIZE_X, player.SQUARE_SIZE_Y))
		else:
			py.draw.rect(screen, (0, 150, 255), py.Rect(player.rect.x - 100, player.rect.y, player.SQUARE_SIZE_X, player.SQUARE_SIZE_Y))

py.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption('Demo')

player1 = Player(300, 150, RED, py.K_a, py.K_d, py.K_SPACE, py.K_LCTRL, 'L')
player2 = Player(800, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_RCTRL, py.K_KP0, 'R')

run = True
clock = py.time.Clock()
while run:
	screen.fill(WHITE)

	line_spacing = 50  # Khoảng cách giữa các đường line
	for y in range(0, SCREEN_HEIGHT, line_spacing):
		py.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))
	line_spacing_vertical = 50
	for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
		py.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))

	for player in [player1, player2]:
		player.draw(screen)
		player.move_logic(py.key.get_pressed())
		player.action(py.key.get_pressed())
		draw_punch_effect(screen, player)

	if player1.punched:
		handle_attack(player1, player2)
	if player2.punched:
		handle_attack(player2, player1)

	for event in py.event.get():
		if event.type == py.QUIT:
			run = False

	py.display.update()
	clock.tick(60)

py.quit()
