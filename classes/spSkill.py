import pygame as py

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

	def skill_use(self, surface, x, active_skill):
		if not active_skill:
			self.spam_l = self.lengt
			self.startX = x
			return False
		# Vẽ hình 1
		for i in range(0, self.lengt - self.spam_l):
			surface.blit(self.hinh_1_list[i], (self.startX + i * 50, 600 - 150))

		# Cập nhật mỗi 10 fps
		self.frame_count += 1
		if self.frame_count % 3 == 0 and self.spam_l > 0 :
			self.spam_l -= 1

		if self.frame_count == 100:
			self.frame_count = 0
			self.spam_l = self.lengt 
			return True
