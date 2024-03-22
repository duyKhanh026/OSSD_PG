import pygame as py
from classes.player import Player

class SPskill1:
	def __init__(self):
		self.image1 = py.image.load("assets/kill1.png")

		# Tạo list để lưu trữ các biến hình
		self.hinh_1_list = []
		self.lengt = int(1200 / 50)
		self.startX = 0

		# Thêm 10 biến hình 1 vào list
		for i in range(0, self.lengt):
			self.hinh_1_list.append(self.image1)
		self.spam = False
		self.spam_l = 0
		self.frame_count = 0
		self.frame_rate = 3

	def skill_use(self, surface, player1, player2):
		if not player1.skill1:
			self.spam_l = self.lengt
			self.startX = player1.rect.x
			return False
		# Vẽ hình 1
		for i in range(0, self.lengt - self.spam_l):
			if player1.side == 'L':
				x = self.startX + i * 50
			else: 
				x = self.startX - i * 50
			y = 600 - 150
			objA = py.Rect(x, y, 50, 150)
			surface.blit(self.hinh_1_list[i], (x, y))
			if (objA.colliderect(player2.rect)):
				player2.get_hit_by_skill = True


		# Cập nhật mỗi 10 fps
		self.frame_count += 1
		if self.frame_count % 3 == 0 and self.spam_l > 0 :
			self.spam_l -= 1

		if self.frame_count == 100:
			self.frame_count = 0
			self.spam_l = self.lengt 
			return True
