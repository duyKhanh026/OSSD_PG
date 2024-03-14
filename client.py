import pygame as py
import socket
import re
from classes.player import Player
from classes.action import *
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

player1 = Player(300, 150, RED, py.K_a, py.K_d, py.K_w, py.K_LCTRL, py.K_e, 'L')
player2 = Player(800, 150, BLUE, None, None, None, None, None, 'R')

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
		player2.rect.x, player2.rect.y, player2.state = parse_input(remesage)
		print(remesage)

attack_cooldown_p1 = 0 
attack_ready_p1 = True
attack_cooldown_p2 = 0
attack_ready_p2 = True

stunned_cooldown_p1 = 0
stunned_ready_p1 = True
stunned_cooldown_p2 = 0
stunned_ready_p2 = True

def flip_coordinates_horizontal(x, y):
    new_x = SCREEN_WIDTH - x
    new_y = y
    return new_x, new_y

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

	player1.move_logic(py.key.get_pressed(), player2)
	player1.action(py.key.get_pressed())
	player1.draw(screen)
	draw_atk_effect(screen, player1)

	if player1.atked:
		if player1 == player1 and attack_ready_p1:
			attack_cooldown_p1 = ATTACK_COOLDOWN
			attack_ready_p1 = False

	player2.draw(screen)
	draw_atk_effect(screen, player2)


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
	x_flip, y_flip = flip_coordinates_horizontal(player1.rect.x, player1.rect.y)
	send(f"({x_flip},{y_flip}) {player1.state}")

py.quit()
send(DISCONNECT_MESSAGE)
