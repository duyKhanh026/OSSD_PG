import pygame as py
import numpy as np
import random
import math
from classes.player import Player
from classes.character1 import Character1
from classes.character2 import Character2
from collections import namedtuple
from classes.action import *
from values.color import *
from values.screen import *


def distance(x1, y1, x2, y2):
	return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class Offline_AI:
	def __init__(self):
		py.init()
		self.reset()

	def reset(self):
		self.count_frame = 0
		self.game_over = False
		self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		py.display.set_caption('Demo')
		self.point = self.random_point()
		self.point_AI =  self.random_point()
		self.player1 = Character1(200, 50, 'blue/stickman_blade', self.point[0], self.point[1], RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L')
		self.player2 = Character2(200, 80, 'purple/stickman', self.point_AI[0], self.point_AI[1], BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_KP1, py.K_KP2, py.K_KP3, py.K_KP4, 'R')
		self.player1.name = 'player1'
		self.player2.name = 'player2'
		self.player_distance = distance(self.player1.rect.x,self.player1.rect.y,self.player2.rect.x,self.player2.rect.y)
		self.clock = py.time.Clock()
		bg = py.image.load(f'assets/mapgame.jpg')
		self.bg1 = py.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
		self.score = 0
		self.hitpoint = False

	def random_point(self):
		x = random.randint(180, SCREEN_WIDTH - 300)

		y = random.randint(200, SCREEN_HEIGHT // 2)

		return [x, y]

	# thực hiện xác nhận player thực hiện đánh thường hoặc đá
	def attack_confirmation(self, player, x, y):
		if player.attack_cooldown_p1 > 0:
			draw_attack_cooldown(self.screen, player.attack_cooldown_p1, (x, y))
			player.attack_cooldown_p1 -= self.clock.get_time()
		elif player.state == 'ATK' or player.state == 'KIC':
			player.attack_ready_p1 = True
			player.attack_cooldown_p1 = 0
			player.state = 'NO'
		else: 
			draw_attack_ready(self.screen, (x, y))

	# xác nhận player bị choáng
	def stunning_confirmation(self, player, x, y):
		if player.stunned_cooldown_p1 > 0:
			draw_stunned_cooldown(self.screen, player.stunned_cooldown_p1, (x, y))
			player.stunned_cooldown_p1 -= self.clock.get_time()
		elif not player.stunned_ready_p1:
			player.stunned_ready_p1 = True
			player.JUMP_POWER = -15
		else:
			draw_stunned_ready(self.screen, (x, y)) 

	# xác nhận player bị đá 
	def kicked_confirmation(self, player, x, y):
		if player.push_cooldown_p1 > 0:
			draw_push_cooldown(self.screen, player.push_cooldown_p1, (x, y))
			player.push_cooldown_p1 -= self.clock.get_time()
		elif not player.push_ready_p1:
			player.push_ready_p1 = True
			player.state = 'NO'
		else:
			draw_push_ready(self.screen, (x, y))

	# gán phía bị đẩy cho player
	def pushed_side(self, p1, p2):
		if p1.side == 'L':
			p2.state = 'PUS_R'  # đẩy về phía bên phải
		else:
			p2.state = 'PUS_L'  # đẩy về phía bên trái
	
	# xữ lý player2 khi player1 dùng đòn đá thành công
	def player_kick(self, p1, p2):
		if p1.state == 'KIC' and p2.state != 'ATK':
			if p1.kicAcount > 30 and p2.state != 'PUS_R' and p2.state != 'PUS_L':
				if handle_attack(p1, p2):
					self.pushed_side(p1, p2)
					p2.velocity_x = 8.4
					p2.push_cooldown_p1 = PUSH_COOLDOWN
					p2.push_ready_p1 = False

	# xữ lý player2 khi player1 dùng đòn đánh thường thành công
	def player_attack(self ,p1, p2):
		if p1.state == 'ATK' and p2.state != 'DEF':
			# print(p1.atkAcount)
			if p1.atkAcount == 16 and p2.state != 'STUN':
				if handle_attack(p1, p2):
					p2.state = 'STUN'
					p2.stunned_cooldown_p1 = STUNNED_COOLDOWN
					p2.stunned_ready_p1 = False
					p2.on_ground = False
					self.pushed_side(p1, p2)
					return True
		return False

	def _update_ui(self):
		self.screen.fill(BLACK)
		self.screen.blit(self.bg1, (0, 0))

		# # Vẽ hình chữ nhật mờ trong suốt
		# bg_rect = py.Surface((SCREEN_WIDTH - 500, SCREEN_HEIGHT), py.SRCALPHA)
		# bg_rect.fill((157, 157, 157, 0))  # Màu với alpha = 128
		# self.screen.blit(bg_rect, (250, 600))  # Vị trí và kích thước của hình chữ nhật

		# bg_rect = py.Surface((SCREEN_WIDTH - 1350, SCREEN_HEIGHT-750), py.SRCALPHA)
		# bg_rect.fill((157, 157, 157, 0))  # Màu với alpha = 128
		# self.screen.blit(bg_rect, (100, 400))  # Vị trí và kích thước của hình chữ nhật

		# bg_rect = py.Surface((SCREEN_WIDTH - 1200, SCREEN_HEIGHT-700), py.SRCALPHA)
		# bg_rect.fill((157, 157, 157, 0))  # Màu với alpha = 128
		# self.screen.blit(bg_rect, (650, 250))  # Vị trí và kích thước của hình chữ nhật 

		# bg_rect = py.Surface((SCREEN_WIDTH - 1250, SCREEN_HEIGHT-700), py.SRCALPHA)
		# bg_rect.fill((157, 157, 157, 0))  # Màu với alpha = 128
		# self.screen.blit(bg_rect, (1150, 350))  # Vị trí và kích thước của hình chữ nhật 
		
		
	

		# xữ lý đầu vào để di chuyển và thực hiện hành động cho nhân vật 
		for player in [self.player1, self.player2]:
			player.move_logic(py.key.get_pressed())
			player.sp_move(py.key.get_pressed())

			if player.state == 'ATK' or player.state == 'KIC':
				if player.attack_cooldown_p1 == 0:
					player.attack_cooldown_p1 = ATTACK_COOLDOWN
					player.attack_ready_p1 = False

		if self.player1.skill_active(self.screen, self.player2):
			handle_attack(None, self.player2)
			self.pushed_side(self.player1, self.player2)

		self.attack_confirmation(self.player1, 10, 30)
		self.attack_confirmation(self.player2, SCREEN_WIDTH - 110, 30)

		self.player_attack(self.player1, self.player2)
		# if self.player_attack(self.player2, self.player1):
		# 	self.score += 1
		# 	self.hitpoint = True


		self.hitpoint = self.player_attack(self.player2, self.player1)

		self.player_kick(self.player1, self.player2)
		self.player_kick(self.player2, self.player1)

		self.stunning_confirmation(self.player1, 10, 50)
		self.stunning_confirmation(self.player2, SCREEN_WIDTH - 110, 50)

		self.kicked_confirmation(self.player1, 10, 80)
		self.kicked_confirmation(self.player2, SCREEN_WIDTH - 110, 80)

	def move_player(self, action):
		if np.array_equal(action, [1, 0, 0]) and self.player2.state != 'ATK' and self.player2.state != 'KIC':
			self.player2.go_left()
		elif np.array_equal(action, [0, 1, 0]) and self.player2.state != 'ATK' and self.player2.state != 'KIC':
			self.player2.go_right()
		elif self.player2.Max_jump > 0 and self.player2.state != 'ATK' and self.player2.state != 'KIC':
			self.player2.do_jump()

	def run(self, action=None):

		# temp = False

		reward = 0

		# Khuyến khích agent bằng việc lại gần nhân vật
		new_player_distance = distance(self.player1.rect.x,self.player1.rect.y,self.player2.rect.x,self.player2.rect.y)
		if new_player_distance <= 150:
			self.score += 1
			# temp = True
			self.count_frame = 0
			reward = 10

			if self.player2.state == 'NO' and self.player2.on_ground:
				move = random.randint(0, 2)
				if move == 0:
					self.player2.do_atk()
				elif move == 1:
					self.player2.do_kic()
				elif move == 2:
					self.player2.do_def()
			

				
			# self.point = self.random_point()
			# self.player1.rect.x = self.point[0]
			# self.player1.rect.y = self.point[1]

		else :
			reward = -5


		# if self.hitpoint:
		# 	self.score += 2
		# 	self.hitpoint = False # Chạm vào ng player
		


		for event in py.event.get():
			if event.type == py.QUIT:
				py.quit()
				quit()


		# if self.count_frame >= 240 and temp == False:
		# 	self.game_over = True
		# 	reward -= 10
		# else :
		# 	self.count_frame += 1


		if self.player2.rect.y > SCREEN_HEIGHT - 150:
			self.game_over = True
			reward -= 10

		
		# print(f'reward: {reward}, distance: {new_player_distance}')
		done = self.game_over


		self._update_ui()

		if action != None:
			self.move_player(action)

		for player in [self.player1, self.player2]:
			player.draw(self.screen)
		
		self.clock.tick(60)
		py.display.update()



		return reward, done, self.score

	def start(self):
		while not self.game_over:
			self.run()