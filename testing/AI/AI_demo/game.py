from player import *

Point = namedtuple('Point', 'x, y')

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Simple Platformer")
		self.clock = pygame.time.Clock()
		self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50, 10, 10)
		self.wall1 = pygame.Rect(300, 300, 20, 50)
		self.point_color = GREEN
		self.score = 0
		self.game_over = False
		self.last_point_time = time.time()
		self.countdown_time = 2
		self.point = self.random_point()

	def random_point(self):
		min_x1 = 50
		max_x1 = self.wall1.x - 50
		min_x2 = self.wall1.y + self.wall1.width + 50
		max_x2 = SCREEN_WIDTH - 80

		if random.choice([True, False]):
			x = random.randint(min_x1, max_x1)
		else:
			x = random.randint(min_x2, max_x2)

		y = random.randint(150, SCREEN_HEIGHT // 2)
		return [x, y]

	def reset(self):
		self.player.x = SCREEN_WIDTH // 2
		self.player.y = SCREEN_HEIGHT // 2
		self.score = 0
		self.game_over = False
		self.last_point_time = time.time()
		self.point = self.random_point()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return True
		return False

	def move_player(self, action):
		if np.array_equal(action, [1, 0, 0]):
			self.player.move_left()
		elif np.array_equal(action, [0, 1, 0]):
			self.player.move_right()
		elif self.player.is_jump:
			self.player.jump()
		self.player.update()

	def check_collision(self):
		player_point = Point(self.player.x, self.player.y)
		if self.player.is_collision(player_point, self.wall1):
			self.game_over = True

	def check_point_collision(self):
		if (self.player.x < self.point[0] + 20 and self.player.x + self.player.size > self.point[0] and
				self.player.y < self.point[1] + 20 and self.player.y + self.player.size > self.point[1]):
			self.score += 1
			self.point = self.random_point()
			self.last_point_time = time.time()

	def play_step(self, action, highest_score):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		self.move_player(action)
		self.check_collision()
		self.check_point_collision()

		if time.time() - self.last_point_time > self.countdown_time:
			self.game_over = True

		reward = 0
		if self.game_over:
			reward = -10
		elif self.score > 0:
			reward = 10
		done = self.game_over

		self._update_ui(highest_score)
		
		self.clock.tick(120)

		return reward, done, self.score


	def _update_ui(self, highest_score):
		self.screen.fill(WHITE)
		pygame.draw.rect(self.screen, (0,0,0), (0, (SCREEN_HEIGHT // 2) + 50, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
		pygame.draw.rect(self.screen, (0,0,255), self.wall1)
		self.player.draw(self.screen)
		pygame.draw.rect(self.screen, self.point_color, (self.point[0], self.point[1], 20, 20))

		font = pygame.font.Font(None, 36)
		score_text = font.render(f"Score: {self.score}", True, RED)
		highest_score_text = font.render(f"Highest Score: {highest_score}", True, RED)
		self.screen.blit(score_text, (10, 10))
		self.screen.blit(highest_score_text, (10, 50))

		time_left = max(0, int(self.countdown_time - (time.time() - self.last_point_time)))
		timer_text = font.render(f"Time Left: {time_left}", True, RED)
		self.screen.blit(timer_text, (10, 90))

		pygame.display.update()