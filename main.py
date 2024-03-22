import pygame as py
from classes.player import Player
from classes.action import *
from classes.spSkill import *
from values.color import *
from values.screen import *

py.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption('Demo')

player1 = Player( 'blue/stickman_blade',300, 150, RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L',)
player2 = Player( 'purple/stickman',900, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_KP1, py.K_KP2, py.K_KP3, py.K_KP4,'R')


spkillp1 = SPskill1() 
spkillp2 = SPskill1()

run = True
clock = py.time.Clock()
while run:
	screen.fill(BLACK)

	line_spacing = 50  # Khoảng cách giữa các đường line
	for y in range(0, SCREEN_HEIGHT, line_spacing):
		py.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))
	line_spacing_vertical = 50
	for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
		py.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))

	player2.get_hit_by_skill = False
	if spkillp1.skill_use(screen, player1, player2): 
		player1.skill1 = False
		player1.state = 'NO'
		player1.sp1count = 0
	# if spkillp2.skill_use(screen, player2, player1): 
	# 	player2.skill1 = False
	# 	player2.state = 'NO'
	# 	player2.sp1count = 0
	if player2.get_hit_by_skill:
		player2.JUMP_POWER = -10 - (100-player2.health)/7
		handle_attack(None, player2)
		player2.velocity_x = 10 + (100-player2.health)/7 # đẩy ra 
		player2.square_y_speed = player2.JUMP_POWER # ép nó nhảy lên
		player2.on_ground = False # trọng lực
	else: 
		player2.JUMP_POWER = -15

	for player in [player1, player2]:
		# draw_atk_effect(screen, player)
		player.move_logic(py.key.get_pressed())
		player.action(py.key.get_pressed())
		player.draw(screen)

		if player.state == 'ATK' or player.state == 'KIC':
			if player.attack_cooldown_p1 == 0:
				player.attack_cooldown_p1 = ATTACK_COOLDOWN
				player.attack_ready_p1 = False

	# Tính thời gian hồi đòn đánh thường
	for player in [player1, player2]:
		if player.attack_cooldown_p1 > 0:
			draw_attack_cooldown(screen, player.attack_cooldown_p1, (10 if player == player1 else SCREEN_WIDTH - 110, 30))
			player.attack_cooldown_p1 -= clock.get_time()
		elif player.state == 'ATK' or player.state == 'KIC':
			player.attack_ready_p1 = True
			player.attack_cooldown_p1 = 0
			player.state = 'NO'
		else: 
			draw_attack_ready(screen, (10 if player == player1 else SCREEN_WIDTH - 110, 30))

	if check_collision(player1, player2):

		# Xử lý khi player1 hoặc player2 tung đòn đá để đẩy
		for player in [player1, player2]:
			if player.state == 'KIC' and (player2.state if player == player1 else player1.state) != 'ATK':
				if player.kicAcount > 30 and (player2.state if player == player1 else player1.state) != 'PUS':
					handle_attack(player1 if player == player1 else player2, player2 if player == player1 else player1)
					if player == player1: 
						player2.state = 'PUS' 
					else: 
						player1.state = 'PUS'

					if player == player1:
					    player2.push_cooldown_p1 = PUSH_COOLDOWN
					else:
					    player1.push_cooldown_p1 = PUSH_COOLDOWN

					if player == player1:
					    player2.push_ready_p1 = False
					else:
					    player1.push_ready_p1 = False

		if player1.state == 'ATK' and player2.state != 'DEF':
			if player1.atkAcount == 16 and player2.state != 'STUN':
				handle_attack(player1, player2)
				player2.state = 'STUN'
				player2.stunned_cooldown_p1 = STUNNED_COOLDOWN
				player2.JUMP_POWER = -10 - (100-player2.health)/7
				player2.stunned_ready_p1 = False
				handle_attack(None, player2)
				player2.velocity_x = 10 + (100-player2.health)/7 # đẩy ra 
				player2.square_y_speed = player2.JUMP_POWER # ép nó nhảy lên
				player2.on_ground = False # trọng lực
		


		if player2.state == 'ATK' and player1.state != 'DEF':
			if player2.atkAcount > 16 and player1.state != 'STUN':
				handle_attack(player2, player1)
				player1.state = 'STUN'  
				player1.stunned_cooldown_p1 = STUNNED_COOLDOWN
				player1.stunned_ready_p1 = False
				

	# Tính thời gian hồi lại khi bị đánh
	for player in [player1, player2]:
		if player.stunned_cooldown_p1 > 0:
			draw_stunned_cooldown(screen, player.stunned_cooldown_p1, (10 if player == player1 else SCREEN_WIDTH - 110, 50))
			player.stunned_cooldown_p1 -= clock.get_time()
		elif not player.stunned_ready_p1:
			player.stunned_ready_p1 = True
			player.state = 'NO'
			player.JUMP_POWER = -15
		else:
			draw_stunned_ready(screen, (10 if player == player1 else SCREEN_WIDTH - 110, 50)) 

	# Tính thời gian hồi lại khi bị đá
	for player in [player2, player1]:
		if player.push_cooldown_p1 > 0:
			draw_push_cooldown(screen, player.push_cooldown_p1, (10 if player == player1 else SCREEN_WIDTH - 110, 80))
			player.push_cooldown_p1 -= clock.get_time()
		elif not player.push_ready_p1:
			player.push_ready_p1 = True
			player.state = 'NO'
		else:
			draw_push_ready(screen, (10 if player == player1 else SCREEN_WIDTH - 110, 80))

	for event in py.event.get():
		if event.type == py.QUIT:
			run = False

	py.display.update()
	clock.tick(60)

	# print(str(player1))

py.quit()
