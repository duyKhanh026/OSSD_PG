import pygame as py

class Player:
	def __init__(self, x, y, color, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key,side):
		self.walkRight = []
		for i in range(1, 6):
			img = py.image.load(f'assets/blue/stickman_blade_running{i}.png')
			self.walkRight.append(img)
		self.slashA = []
		for i in range(1, 8):
			img = py.image.load(f'assets/blue/stickman_blade_slash{i if i < 6 else 5}.png')
			self.slashA.append(img)

		self.kickA = []
		for i in range(1, 8):
			img = py.image.load(f'assets/blue/stickman_blade_kick{i}.png')
			self.kickA.append(img)

		self.charIdle = py.image.load('assets/blue/stickman_blade_idle.png')
		self.defenseA = py.image.load('assets/blue/stickman_blade_defense.png')
		self.sp1 = []

		for i in range(1, 20):
			img = py.image.load(f'assets/blue/stickman_blade_sp{i}.png')
			self.sp1.append(img)
		self.walkCount = 0
		self.skill1 = False
		self.sp1count = 0
		self.sp1_key = sp1_key
		self.right = True if side == 'L' else False
		self.left = True if side == 'R' else False

		self.SQUARE_SIZE_X = 100
		self.SQUARE_SIZE_Y = 150
		self.rect = py.Rect(x, y, self.SQUARE_SIZE_X, self.SQUARE_SIZE_Y)
		self.color = color
		self.move_left_key = move_left_key
		self.move_right_key = move_right_key
		self.side = side  # Dùng để phân biệt phía của player
		self.speed = 4
		self.Max_jump = 2
		self.jump_count = 0

		# Use for jump event
		self.jump_key = jump_key
		self.on_ground = False
		self.square_y_speed = 0
		self.GRAVITY = 0.5
		self.JUMP_POWER = -15

		self.state = 'NO'

		# Use for Attack
		self.atk_key = atk_key
		self.attack_cooldown_p1 = 0 
		self.attack_ready_p1 = True
		self.atkAcount = 0 #for animation

		# Use for being attacked
		self.stunned_cooldown_p1 = 0
		self.stunned_ready_p1 = True

		# Use for being kicked
		self.push_cooldown_p1 = 0
		self.push_ready_p1 = True

		# Use for Defense
		self.def_key = def_key

		# Use for Kick
		self.kic_key = kick_key
		self.kicAcount = 0 #for animation

		# Health bar
		self.max_health = 100
		self.health = self.max_health

		self.velocity_x = 0
		self.pushed = False


	def redrawGameWindow(self, surface):
		if self.walkCount + 1 >= 30:
			self.walkCount = 0
		if self.atkAcount + 1 >= 42 or self.state != 'ATK':
			self.atkAcount = 0
		if self.kicAcount + 1 >= 42 or self.state != 'KIC':
			self.kicAcount = 0
		if self.sp1count >= 113:
			self.skill1 = True
			self.sp1count = 113
			
		if self.state == 'SP1':
			surface.blit(self.sp1[self.sp1count//6] if self.side == 'L' else py.transform.flip(self.sp1[self.sp1count//6], True, False), (self.rect.x - self.SQUARE_SIZE_X * (2 if self.side == 'L' else 1), self.rect.y - 100))
			if self.sp1count < 113:
				self.sp1count += 1
		elif self.state == 'ATK':
			surface.blit(self.slashA[self.atkAcount//6] if self.side == 'L' else py.transform.flip(self.slashA[self.atkAcount//6], True, False), (self.rect.x - self.SQUARE_SIZE_X * (2 if self.side == 'L' else 1), self.rect.y))
			self.atkAcount += 1
		elif self.state == 'KIC':
			surface.blit(self.kickA[self.kicAcount//6] if self.side == 'L' else py.transform.flip(self.kickA[self.kicAcount//6], True, False), (self.rect.x - self.SQUARE_SIZE_X * (2 if self.side == 'L' else 1), self.rect.y))
			self.kicAcount += 1
		elif self.right:
			surface.blit(self.walkRight[self.walkCount//6], (self.rect.x - self.SQUARE_SIZE_X * (2 if self.side == 'L' else 1), self.rect.y))
			self.walkCount += 1
		elif self.left:
			surface.blit(py.transform.flip(self.walkRight[self.walkCount//6], True, False), (self.rect.x - self.SQUARE_SIZE_X * (2 if self.side == 'L' else 1), self.rect.y))
			self.walkCount += 1
		elif self.state == 'DEF':
			surface.blit(self.defenseA if self.side == 'L' else py.transform.flip(self.defenseA, True, False), (self.rect.x - self.SQUARE_SIZE_X * (2 if self.side == 'L' else 1), self.rect.y))
		else :
			surface.blit(self.charIdle if self.side == 'L' else py.transform.flip(self.charIdle, True, False), (self.rect.x - self.SQUARE_SIZE_X * (2 if self.side == 'L' else 1), self.rect.y))

	def move(self, dx, dy):
		self.rect.move_ip(dx, dy)

	def draw(self, surface):
		# if self.side == 'R':
		# 	py.draw.rect(surface, self.color, self.rect)
		# else:
		# 	py.draw.rect(surface, self.color, py.Rect(self.rect.x - self.SQUARE_SIZE_X, self.rect.y, self.SQUARE_SIZE_X, self.SQUARE_SIZE_Y))


		self.redrawGameWindow(surface)

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
		
		# Draw text about the current state 
		# font = py.font.SysFont(None, 46)
		# text = font.render(' ' + self.state, True, (255, 255,255))
		# surface.blit(text, (self.rect.x if self.side == 'R' else self.rect.x - self.SQUARE_SIZE_X, self.rect.y + self.SQUARE_SIZE_Y // 2))

	def action(self, key):
		if self.move_left_key == None:
			return 

		if key[self.sp1_key]:
			self.state = 'SP1'
			self.sp1count = 0
		elif self.state != 'ATK' and self.state != 'KIC' and self.state != 'STUN' and self.state != 'SP1':
			if key[self.atk_key]:
				self.atkAcount = 0
				self.state = 'ATK'
			elif key[self.def_key]:
				self.state = 'DEF'
			elif key[self.kic_key]:
				self.kicAcount = 0
				self.state = 'KIC'
			else:
				self.state = 'NO'

	def move_logic(self, key):

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

		if self.state == 'PUS' and not self.pushed:
			self.pushed = True
			self.velocity_x = 10

		if self.side == 'R':
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
			self.pushed = False
		
		# Kiểm tra không cho khối vuông đi ra ngoài màn hình bên trái
		if self.rect.left < 0:
			self.rect.left = 0
			self.velocity_x = 0  # Đặt tốc độ thành 0 nếu chạm cạnh bên trái của màn hình
			self.pushed = False 

		if self.move_left_key == None:
			return 
		if self.state == 'DEF' or self.state == 'SP1' or self.state == 'STUN':
			return
		if key[self.move_left_key]:
			self.right = False
			if self.side == 'L':
				self.rect.x -= self.SQUARE_SIZE_X
			self.side = 'R'
			self.left = True
			self.move(-self.speed, 0)
		elif key[self.move_right_key]:
			self.right = True
			if self.side == 'R':
				self.rect.x += self.SQUARE_SIZE_X
			self.side = 'L'
			self.left = False
			self.move(self.speed, 0)
		else:
			self.right = False
			self.left = False
		if key[self.jump_key] and self.on_ground:
			self.square_y_speed = self.JUMP_POWER
			self.on_ground = False



		# if self.side == 'L' and self.rect.y >= pl2.rect.y - pl2.SQUARE_SIZE_Y and self.rect.y <= pl2.rect.y:
		# 	if self.rect.x > pl2.rect.x and self.rect.x <= pl2.rect.x + pl2.SQUARE_SIZE_X:
		# 		self.move(-self.speed, 0)
		# 	elif self.rect.x < pl2.rect.x + pl2.SQUARE_SIZE_X * 2 and self.rect.x > pl2.rect.x + pl2.SQUARE_SIZE_X:
		# 		self.move(self.speed, 0)


	def __str__(self):
		# Tạo một chuỗi đại diện cho đối tượng Player
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
			str(self.side)
		]
		return ",".join(player_info)

	def from_string(self, player_str):
		# Tách chuỗi để lấy các giá trị
		values = player_str.split(",")
		# Gán các giá trị cho các thuộc tính của đối tượng Player
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
		self.side = 'L' if values[14] == 'R' else 'R' # đảo lại phía cho p2
		self.rect.x = 1200 - self.rect.x # đổi vị trí của từ p1 sang p2