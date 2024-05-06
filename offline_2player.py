import pygame as py
import numpy as np
from classes.player import Player
from classes.character1 import Character1
from classes.character2 import Character2
from classes.action import *
from values.color import *
from values.screen import *

class Offline_2player:
	def __init__(self):
		py.init()
		self.count_frame = 0
		self.game_over = 0
		self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		py.display.set_caption('Fighting Game')
		self.player1 = Character1(200, 50, 'blue/stickman_blade', 300, 150, RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L')
		self.player2 = Character2(200, 80, 'purple/stickman', 1200, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_KP1, py.K_KP2, py.K_KP3, py.K_KP4, 'R')
		self.player1.name = 'player1'
		self.player2.name = 'player2'
		self.clock = py.time.Clock()
		bg = py.image.load(f'assets/bg2.jpg')
		self.bg1 = py.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
		self.score = 0

	def reset(self):
		self.count_frame = 0
		self.game_over = 0
		self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		py.display.set_caption('Demo')
		self.player1 = Character1(200, 50, 'blue/stickman_blade', 300, 150, RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L')
		self.player2 = Character2(200, 80, 'purple/stickman', 1200, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_KP1, py.K_KP2, py.K_KP3, py.K_KP4, 'R')
		self.player1.name = 'player1'
		self.player2.name = 'player2'
		self.clock = py.time.Clock()
		bg = py.image.load(f'assets/bg2.jpg')
		self.bg1 = py.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
		self.score = 0

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
		py.draw.rect(self.screen, (157,157,157), py.Rect(200, 600, SCREEN_WIDTH - 400, SCREEN_HEIGHT))
		# vẽ sọc trắng lên màn hình
		line_spacing = 50
		for y in range(0, SCREEN_HEIGHT, line_spacing):
			py.draw.line(self.screen, WHITE, (0, y), (SCREEN_WIDTH, y))
		line_spacing_vertical = 50
		for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
			py.draw.line(self.screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))

		# self.screen.blit(self.bg1, (0,0))

		# xữ lý đầu vào để di chuyển và thực hiện hành động cho nhân vật 
		for player in [self.player1, self.player2]:
			player.move_logic(py.key.get_pressed())
			player.sp_move(py.key.get_pressed())

			if player.state == 'ATK' or player.state == 'KIC':
				if player.attack_cooldown_p1 == 0:
					player.attack_cooldown_p1 = ATTACK_COOLDOWN
					player.attack_ready_p1 = False

			if player.rect.y > SCREEN_HEIGHT:
				self.game_over = (1 if player == self.player1 else 2) 
			elif player.health <= 0:
				self.game_over = (1 if player == self.player1 else 2) 

		if self.player1.skill_active(self.screen, self.player2):
			handle_attack(None, self.player2)
			self.pushed_side(self.player1, self.player2)

		self.attack_confirmation(self.player1, 10, 30)
		self.attack_confirmation(self.player2, SCREEN_WIDTH - 110, 30)

		self.player_attack(self.player1, self.player2)
		if self.player_attack(self.player2, self.player1):
			self.score += 1
			self.hitpoint = True

		self.player_kick(self.player1, self.player2)
		self.player_kick(self.player2, self.player1)

		self.stunning_confirmation(self.player1, 10, 50)
		self.stunning_confirmation(self.player2, SCREEN_WIDTH - 110, 50)

		self.kicked_confirmation(self.player1, 10, 80)
		self.kicked_confirmation(self.player2, SCREEN_WIDTH - 110, 80)

	def run(self, action=None):
		for event in py.event.get():
			if event.type == py.QUIT:
				py.quit()
				quit()
		if self.game_over == 0:
			self._update_ui()

			for player in [self.player1, self.player2]:
				player.draw(self.screen)
		else :
			textEnd = "PLAYER 1 WIN" if self.game_over == 2 else "PLAYER 2 WIN"
			text = py.font.SysFont(None, 64).render(textEnd, True, WHITE)
			text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
			self.screen.blit(text, text_rect)


		self.clock.tick(60)
		py.display.update()



	def start(self):
		while True:
			self.run()