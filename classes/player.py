import pygame as py

class Player:
	def __init__(self, x, y, color, move_left_key, move_right_key, jump_key, punch_key, side):
		self.SQUARE_SIZE_X = 100
		self.SQUARE_SIZE_Y = 150
		self.rect = py.Rect(x, y, self.SQUARE_SIZE_X, self.SQUARE_SIZE_Y)
		self.color = color
		self.move_left_key = move_left_key
		self.move_right_key = move_right_key
		self.side = side  # Dùng để phân biệt phía của player
		self.speed = 4

		# Use for jump event
		self.jump_key = jump_key
		self.on_ground = False
		self.square_y_speed = 0
		self.GRAVITY = 0.5
		self.JUMP_POWER = -15

		# Use for punch
		self.punch_key = punch_key
		self.punched = False

		# Health bar
		self.max_health = 100
		self.health = self.max_health

	def move(self, dx, dy):
		self.rect.move_ip(dx, dy)

	def draw(self, surface):
		if self.side == 'R':
			py.draw.rect(surface, self.color, self.rect)
		else:
			py.draw.rect(surface, self.color, py.Rect(self.rect.x - self.SQUARE_SIZE_X, self.rect.y, self.SQUARE_SIZE_X, self.SQUARE_SIZE_Y))

		py.draw.line(surface, (26, 243, 0), (self.rect.x, 0), (self.rect.x, 600))
		py.draw.line(surface, (26, 243, 0), (0, self.rect.y), (1200, self.rect.y))
		font = py.font.SysFont(None, 16)
		text = font.render(' (' + str(self.rect.x) + ',' + str(self.rect.y) + ')', True, (0, 0, 0))
		surface.blit(text, (self.rect.x, 10))

		# Draw health bar
		if self.side == 'R':
			py.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 20, self.SQUARE_SIZE_X, 10))
			py.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 20, int(self.SQUARE_SIZE_X * (self.health / self.max_health)), 10))
		else :
			py.draw.rect(surface, (255, 0, 0), (self.rect.x - self.SQUARE_SIZE_X, self.rect.y - 20, self.SQUARE_SIZE_X, 10))
			py.draw.rect(surface, (0, 255, 0), (self.rect.x - self.SQUARE_SIZE_X, self.rect.y - 20, int(self.SQUARE_SIZE_X * (self.health / self.max_health)), 10))
		
	def action(self, key):
		if key[self.punch_key] :
			self.punched = True
		else:
			self.punched = False

	def move_logic(self, key):
		if key[self.move_left_key]:
			self.move(-self.speed, 0)
		elif key[self.move_right_key]:
			self.move(self.speed, 0)
		if key[self.jump_key] and self.on_ground:
			self.square_y_speed = self.JUMP_POWER
			self.on_ground = False

		# Áp dụng trọng lực
		self.square_y_speed += self.GRAVITY
		self.rect.y += self.square_y_speed

		# Kiểm tra va chạm với mặt đất
		if self.rect.y >= 600 - self.SQUARE_SIZE_Y:
			self.rect.y = 600 - self.SQUARE_SIZE_Y
			self.square_y_speed = 0
			self.on_ground = True

		# Giới hạn không cho khối vuông đi quá biên
		if self.side == 'R':
			if self.rect.x < 0:
				self.rect.x = 0
			elif self.rect.x > 1200 - self.SQUARE_SIZE_X:
				self.rect.x = 1200 - self.SQUARE_SIZE_X
		else:
			if self.rect.x < self.SQUARE_SIZE_X:
				self.rect.x = self.SQUARE_SIZE_X
			elif self.rect.x > 1200:
				self.rect.x = 1200





