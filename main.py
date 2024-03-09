import pygame as py
from classes.player import Player
from values.color import *
from values.screen import *

ATTACK_COOLDOWN = 500  # Thời gian hồi của đòn đánh (milliseconds)
DAMAGE = 10

def check_collision(p1, p2):
	return p1.rect.colliderect(p2.rect)

def handle_attack(attacker, victim):
	if check_collision(attacker, victim):
		victim.health -= DAMAGE

def draw_punch_effect(screen, player):
	if player.punched:
		if player.side == 'L':
			py.draw.rect(screen, (255, 150, 0), py.Rect(player.rect.x, player.rect.y, player.SQUARE_SIZE_X, player.SQUARE_SIZE_Y))
		else:
			py.draw.rect(screen, (0, 150, 255), py.Rect(player.rect.x - 100, player.rect.y, player.SQUARE_SIZE_X, player.SQUARE_SIZE_Y))

def draw_attack_cooldown(screen, time_remaining, toado):
	font = py.font.SysFont(None, 24)
	text = font.render(f'Attack: {time_remaining / 1000:.1f} s', True, (0, 0, 0))
	screen.blit(text, toado)

def draw_ready(screen, toado):
	font = py.font.SysFont(None, 24)
	text = font.render('Attack: Ready', True, (0, 0, 0))
	screen.blit(text, toado)

py.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption('Demo')

player1 = Player(300, 150, RED, py.K_a, py.K_d, py.K_SPACE, py.K_LCTRL, 'L')
player2 = Player(800, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_RCTRL, py.K_KP0, 'R')

attack_cooldown_p1 = 0
attack_ready_p1 = True
attack_cooldown_p2 = 0
attack_ready_p2 = True

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

		if player.punched:
			if player == player1 and attack_ready_p1:
				attack_cooldown_p1 = ATTACK_COOLDOWN
				handle_attack(player1, player2)
				attack_ready_p1 = False
			elif player == player2 and attack_ready_p2:
				attack_cooldown_p2 = ATTACK_COOLDOWN
				handle_attack(player2, player1)
				attack_ready_p2 = False

	if attack_cooldown_p1 > 0:
		draw_attack_cooldown(screen, attack_cooldown_p1, (10, 30))
		attack_cooldown_p1 -= clock.get_time()
	else:
		draw_ready(screen, (10, 30))
		attack_ready_p1 = True

	if attack_cooldown_p2 > 0:
		draw_attack_cooldown(screen, attack_cooldown_p2, (SCREEN_WIDTH - 110, 30))
		attack_cooldown_p2 -= clock.get_time()
	else:
		draw_ready(screen, (SCREEN_WIDTH - 110, 30))
		attack_ready_p2 = True

	for event in py.event.get():
		if event.type == py.QUIT:
			run = False

	py.display.update()
	clock.tick(60)

py.quit()
