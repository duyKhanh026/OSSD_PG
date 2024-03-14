import pygame as py
from classes.player import Player
from classes.action import *
from values.color import *
from values.screen import *

py.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption('Demo')

player1 = Player(300, 150, RED, py.K_a, py.K_d, py.K_w, py.K_LCTRL, py.K_e, 'L')
player2 = Player(800, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_KP0, py.K_KP1, 'R')

attack_cooldown_p1 = 0 
attack_ready_p1 = True
attack_cooldown_p2 = 0
attack_ready_p2 = True

stunned_cooldown_p1 = 0
stunned_ready_p1 = True
stunned_cooldown_p2 = 0
stunned_ready_p2 = True


run = True
clock = py.time.Clock()
vong = 0
while run:
	screen.fill(WHITE)

	line_spacing = 50  # Khoảng cách giữa các đường line
	for y in range(0, SCREEN_HEIGHT, line_spacing):
		py.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))
	line_spacing_vertical = 50
	for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
		py.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))

	player.move_logic(py.key.get_pressed())
	player.action(py.key.get_pressed())
	player.draw(screen)
	draw_atk_effect(screen, player)

	if player.atked:
		if player == player1 and attack_ready_p1:
			attack_cooldown_p1 = ATTACK_COOLDOWN
			attack_ready_p1 = False
		elif player == player2 and attack_ready_p2:
			attack_cooldown_p2 = ATTACK_COOLDOWN
			attack_ready_p2 = False


	if attack_cooldown_p1 > 0:
		draw_attack_cooldown(screen, attack_cooldown_p1, (10, 30))
		attack_cooldown_p1 -= clock.get_time()
	else:
		draw_attack_ready(screen, (10, 30))
		attack_ready_p1 = True
		player1.atked = False

	if attack_cooldown_p2 > 0:
		draw_attack_cooldown(screen, attack_cooldown_p2, (SCREEN_WIDTH - 110, 30))
		attack_cooldown_p2 -= clock.get_time()
	else:
		draw_attack_ready(screen, (SCREEN_WIDTH - 110, 30))
		attack_ready_p2 = True
		player2.atked = False

	if check_collision(player1, player2):
		if not player1.state == 'DEF' and not player2.state == 'DEF':
			if player1.state == 'ATK' and player2.state == 'NO':
				handle_attack(player1, player2)
				player2.state = 'STUN'
				stunned_cooldown_p2 = STUNNED_COOLDOWN
				stunned_ready_p2 = False
			if player2.state == 'ATK' and player1.state == 'NO':
				handle_attack(player2, player1)
				player1.state = 'STUN'  
				stunned_cooldown_p1 = STUNNED_COOLDOWN
				stunned_ready_p1 = False

	if stunned_cooldown_p1 > 0:
		draw_stunned_cooldown(screen, stunned_cooldown_p1, (10, 50))
		stunned_cooldown_p1 -= clock.get_time()
	elif not stunned_ready_p1:
		stunned_ready_p1 = True
		player1.state = 'NO'
	else:
		draw_stunned_ready(screen, (10, 50)) 

	if stunned_cooldown_p2 > 0:
		draw_stunned_cooldown(screen, stunned_cooldown_p2, (SCREEN_WIDTH - 110, 50))
		stunned_cooldown_p2 -= clock.get_time()
	elif not stunned_ready_p2:
		stunned_ready_p2 = True
		player2.state = 'NO'
	else:
		draw_stunned_ready(screen, (SCREEN_WIDTH - 110, 50))



	for event in py.event.get():
		if event.type == py.QUIT:
			run = False

	py.display.update()
	clock.tick(60)
	vong += 1

py.quit()
