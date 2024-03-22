import pygame as py
import socket
import re
from classes.player import Player
from classes.action import *
from classes.spSkill import *
from values.color import *
from values.screen import *

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

py.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption('Demo')


player1 = Player( 'blue/stickman_blade', 300, 150,  RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L',)
player2 = Player( 'purple/stickman', 800, 150, BLUE,   None,   None,   None,   None,   None,   None, None, 'R')

def parse_input(input_string):
	# Sử dụng biểu thức chính quy để tách tọa độ và chuỗi
	match = re.match(r'\((\d+),(\d+)\)\s*(\w+)', input_string)

	# Nếu tìm thấy sự phù hợp
	if match:
		# Lấy tọa độ x, y và chuỗi
		x = int(match.group(1))
		y = int(match.group(2))
		string = match.group(3)

		# Trả về kết quả
		return x, y, string
	else:
		return None


def flip_coordinates_horizontal(x, y):
	new_x = SCREEN_WIDTH - x
	new_y = y
	return new_x, new_y

def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)
	remesage = client.recv(2048).decode(FORMAT)
	global player2
	if not remesage == 'NOPLAY':
		player2.from_string(remesage)
		print(remesage)



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


	if spkillp1.skill_use(screen, player1.rect.x, player1.skill1): 
		player1.skill1 = False
		player1.state = 'NO'
		player1.sp1count = 0
	if spkillp2.skill_use(screen, player2.rect.x, player2.skill1): 
		player2.skill1 = False
		player2.state = 'NO'
		player2.sp1count = 0

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
			if player != player1 and player.state == 'KIC' and (player2.state if player == player1 else player1.state) != 'ATK':
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

		# if player1.state == 'ATK' and player2.state != 'DEF':
		# 	if player1.atkAcount == 16 and player2.state != 'STUN':
		# 		handle_attack(player1, player2)
		# 		player2.state = 'STUN'
		# 		player2.stunned_cooldown_p1 = STUNNED_COOLDOWN
		# 		player2.stunned_ready_p1 = False

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

	send(str(player1))
	print(str(player2))

py.quit()
send(DISCONNECT_MESSAGE)