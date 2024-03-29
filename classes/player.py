import pygame as py

class Player:
	def __init__(self, hx, hy, strNam, x, y, color, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key, side):
		self.health_bar_x = hx
		self.health_bar_y = hy
		self.load_images(strNam)
		self.set_starting_parameters(x, y, color, side)
		self.set_control_keys(move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key)
		self.set_default_values()

	def load_images(self, strNam):
		self.walkRight = [py.image.load(f'assets/{strNam}_running{i}.png') for i in range(1, 6)]
		self.slashA1 = [py.image.load(f'assets/{strNam}_slash{i}.png') for i in range(1, 5)]
		self.kickA = [py.image.load(f'assets/{strNam}_kick{i}.png') for i in range(1, 8)]
		self.charIdle = [py.image.load(f'assets/{strNam}_idle{i}.png') for i in range(1, 6)]
		self.defenseA = py.image.load(f'assets/{strNam}_defense.png')

	def set_starting_parameters(self, x, y, color, side):
		self.rect = py.Rect(x, y, 100, 150)
		self.color = color
		self.side = side
		self.max_health = 100
		self.health = self.max_health

	def set_control_keys(self, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key):
		self.move_left_key = move_left_key
		self.move_right_key = move_right_key
		self.jump_key = jump_key
		self.atk_key = atk_key
		self.def_key = def_key
		self.kick_key = kick_key
		self.sp1_key = sp1_key

	def set_default_values(self):
		self.speed = 6
		self.GRAVITY = 0.5
		self.sp1count = 0
		self.walkCount = 0
		self.atkAcount = 0
		self.kicAcount = 0
		self.idlecount = 0
		self.velocity_x = 0
		self.JUMP_POWER = -15
		self.square_y_speed = 0
		self.push_cooldown_p1 = 0
		self.attack_cooldown_p1 = 0
		self.stunned_cooldown_p1 = 0
		self.skill1 = False
		self.on_ground = False
		self.push_ready_p1 = True
		self.attack_ready_p1 = True
		self.stunned_ready_p1 = True
		self.get_hit_by_skill = False
		self.state = 'NO'

	def redrawGameWindow(self, surface):
		if self.state == 'ATK':
			if self.atkAcount < 23:
				self.atkAcount += 1
			elif self.atkAcount > 23:
				self.atkAcount = 0
			surface.blit(self.slashA1[self.atkAcount//6] if self.side == 'L' else py.transform.flip(self.slashA1[self.atkAcount//6], True, False), (self.rect.x - self.rect.width * (2 if self.side == 'L' else 1), self.rect.y - 100))
		elif self.state == 'KIC':
			surface.blit(self.kickA[self.kicAcount//6] if self.side == 'L' else py.transform.flip(self.kickA[self.kicAcount//6], True, False), (self.rect.x - self.rect.width * (2 if self.side == 'L' else 1), self.rect.y))
			self.kicAcount += 1
		elif self.right:
			surface.blit(self.walkRight[self.walkCount//6], (self.rect.x - self.rect.width * (2 if self.side == 'L' else 1), self.rect.y))
			self.walkCount += 1
		elif self.left:
			surface.blit(py.transform.flip(self.walkRight[self.walkCount//6], True, False), (self.rect.x - self.rect.width * (2 if self.side == 'L' else 1), self.rect.y))
			self.walkCount += 1
		elif self.state == 'DEF':
			surface.blit(self.defenseA if self.side == 'L' else py.transform.flip(self.defenseA, True, False), (self.rect.x - self.rect.width * (2 if self.side == 'L' else 1), self.rect.y))
		else :
			surface.blit(self.charIdle[self.idlecount//6] if self.side == 'L' else py.transform.flip(self.charIdle[self.idlecount//6], True, False), (self.rect.x - self.rect.width * (2 if self.side == 'L' else 1), self.rect.y - self.rect.height + 50))
			self.idlecount += 1

	def move(self, dx, dy):
		self.rect.move_ip(dx, dy)

	def draw(self, surface):
		# if self.side == 'R':
		# 	py.draw.rect(surface, self.color, self.rect)
		# else:
		# 	py.draw.rect(surface, self.color, py.Rect(self.rect.x - self.rect.width, self.rect.y, self.rect.width, self.rect.height))

		self.redrawGameWindow(surface)
		py.draw.line(surface, (26, 243, 0), (self.rect.x, 0), (self.rect.x, 800))
		py.draw.line(surface, (26, 243, 0), (0, self.rect.y), (1500, self.rect.y))
		font = py.font.SysFont(None, 16)
		text = font.render(' (' + str(self.rect.x) + ',' + str(self.rect.y) + ')', True, (0, 0, 0))
		surface.blit(text, (self.rect.x, 10))

		# Draw health bar
		py.draw.rect(surface, (255, 0, 0), (self.health_bar_x, self.health_bar_y, self.rect.width, 10))
		py.draw.rect(surface, (0, 255, 0), (self.health_bar_x, self.health_bar_y, int(self.rect.width * (self.health / self.max_health)), 10))
		
		# Draw text about the current state 
		# font = py.font.SysFont(None, 46)
		# text = font.render(' ' + self.state, True, (255, 255,255))
		# surface.blit(text, (self.rect.x if self.side == 'R' else self.rect.x - self.rect.width, self.rect.y + self.rect.height // 2))

	def action(self, key):
		if self.move_left_key == None:
			return 

		if key[self.sp1_key]:
			self.state = 'SP1'
			self.sp1count = 0
		elif self.state == 'DEF' or self.state == 'NO':
			if key[self.atk_key]:
				self.atkAcount = 0
				self.state = 'ATK'
			elif key[self.def_key]:
				self.state = 'DEF'
			elif key[self.kick_key]:
				self.kicAcount = 0
				self.state = 'KIC'
			else:
				self.state = 'NO'

	def move_logic(self, key):
		# Áp dụng trọng lực
		if not self.on_ground:
			self.square_y_speed += self.GRAVITY
			self.rect.y += self.square_y_speed

		# Kiểm tra va chạm với mặt đất
		if self.rect.y >= 800 - self.rect.height:
			self.rect.y = 800 - self.rect.height
			self.square_y_speed = 0
			self.on_ground = True

		# Giới hạn không cho khối vuông đi quá biên
		if self.side == 'R':
			if self.rect.x < 0:
				self.rect.x = 0
			elif self.rect.x > 1500 - self.rect.width:
				self.rect.x = 1500 - self.rect.width
		else:
			if self.rect.x < self.rect.width:
				self.rect.x = self.rect.width
			elif self.rect.x > 1500:
				self.rect.x = 1500

		# thực hiện đẩy player theo hướng đá 
		if self.state == 'PUS_R':
			self.rect.x += self.velocity_x
		else :
			self.rect.x -= self.velocity_x

		# Áp dụng ma sát
		if self.velocity_x > 0:
			self.velocity_x -= 0.2  # Giảm tốc độ dương
		elif self.velocity_x < 0:
			self.velocity_x += 0.2  # Giảm tốc độ âm
		if abs(self.velocity_x) < 0.2:
			self.velocity_x = 0  # Đảm bảo tốc độ không trở thành số âm nhỏ
			if self.state == 'PUS_R' or self.state == 'PUS_L':
				self.state = 'NO'
		
		# Kiểm tra không cho khối vuông đi ra ngoài màn hình bên trái
		if self.rect.left < 0:
			self.rect.left = 0
			self.velocity_x = 0  # Đặt tốc độ thành 0 nếu chạm cạnh bên trái của màn hình

		if self.move_left_key == None:
			return 
		if self.state != 'NO' and self.on_ground:
			return

		# kiểm tra input từ bàn phím
		if key[self.move_left_key]:
			self.right = False
			if self.side == 'L':
				self.rect.x -= self.rect.width
			self.side = 'R'
			self.left = True
			self.move(-self.speed, 0)
		elif key[self.move_right_key]:
			self.right = True
			if self.side == 'R':
				self.rect.x += self.rect.width
			self.side = 'L'
			self.left = False
			self.move(self.speed, 0)
		else:
			self.right = False
			self.left = False
		if key[self.jump_key] and self.on_ground:
			self.square_y_speed = self.JUMP_POWER
			self.on_ground = False

	def __str__(self):   # Tạo một chuỗi đại diện cho đối tượng Player
		player_info = [
			str(self.speed),
			str(self.Max_jump),
			str(self.jump_count),
			str(self.on_ground),
			str(self.square_y_speed),
			str(self.GRAVITY),
			str(self.JUMP_POWER),
			self.state,
			str(self.max_health),
			str(self.health),
			str(self.velocity_x),
			str(self.pushed),
			str(self.rect.x),
			str(self.rect.y),
			str(self.side),
			str(self.walkCount),
			str(self.kicAcount),
			str(self.atkAcount),
			str(self.sp1count),
			str(self.idlecount),
			str(self.right),
			str(self.left),
			str(self.imgStr)
		]
		return ",".join(player_info)

	def from_string(self, player_str):  # chuyển string lấy từ server thành giá trị cho player
		values = player_str.split(",")
		self.speed = int(values[0])
		self.Max_jump = int(values[1])
		self.jump_count = int(values[2])
		self.on_ground = values[3].lower() == 'true'
		self.square_y_speed = float(values[4])
		self.GRAVITY = float(values[5])
		self.JUMP_POWER = float(values[6])
		self.state = values[7]
		self.max_health = int(values[8])
		self.health = int(values[9])
		self.velocity_x = float(values[10])
		self.pushed = values[11].lower() == 'true'
		self.rect.x = float(values[12])
		self.rect.y = float(values[13])
		self.side = values[14]
		self.walkCount = int(values[15])
		self.kicAcount = int(values[16])
		self.atkAcount = int(values[17])
		self.sp1count = int(values[18])
		self.idlecount = int(values[19])
		self.right = values[20].lower() == 'true'
		self.left = values[21].lower() == 'true'