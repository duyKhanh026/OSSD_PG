import pygame
import sys
import random
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import time
import os
import torch.nn.functional as F
from collections import namedtuple
import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.figure(figsize=(10, 10))
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


# Định nghĩa các hằng số
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


Point = namedtuple('Point', 'x, y')

class QTrainer:
	def __init__(self, model, lr, gamma):
		self.lr = lr
		self.gamma = gamma
		self.model = model
		self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
		self.criterion = nn.MSELoss()

	def train_step(self, state, action, reward, next_state, done):
		state = torch.tensor(state, dtype=torch.float)
		next_state = torch.tensor(next_state, dtype=torch.float)
		action = torch.tensor(action, dtype=torch.long)
		reward = torch.tensor(reward, dtype=torch.float)

		if len(state.shape) == 1:
			state = torch.unsqueeze(state, 0)
			next_state = torch.unsqueeze(next_state, 0)
			action = torch.unsqueeze(action, 0)
			reward = torch.unsqueeze(reward, 0)
			done = (done, )

		pred = self.model(state)

		target = pred.clone()
		for idx in range(len(done)):
			Q_new = reward[idx]
			if not done[idx]:
				Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

			target[idx][torch.argmax(action[idx]).item()] = Q_new
		self.optimizer.zero_grad()
		loss = self.criterion(target, pred)
		loss.backward()

		self.optimizer.step()

class QNetwork(nn.Module):
	def __init__(self, input_size, output_size):
		super().__init__()
		self.linear1 = nn.Linear(input_size, 128)
		self.linear2 = nn.Linear(128, 64)
		self.linear3 = nn.Linear(64, output_size)

	def forward(self, x):
		x = F.relu(self.linear1(x))
		x = F.relu(self.linear2(x))
		x = self.linear3(x)
		return x

class Player:
	def __init__(self, x, y, size, velocity, jump_strength):
		self.x = x
		self.y = y
		self.size = size
		self.velocity = velocity
		self.jump_strength = jump_strength
		self.is_jump = False
		self.jump_count = 10
		self.color = RED

	def move_left(self):
		self.x -= self.velocity

	def move_right(self):
		self.x += self.velocity

	def jump(self):
		if not self.is_jump:
			self.is_jump = True

	def is_collision(self, pointt, walls):
		if pointt.x <= 0 or pointt.x >= SCREEN_WIDTH - 50:
			self.color = (0, 255, 0)
			return True
		if walls != None:
			if walls.colliderect(pygame.Rect(pointt.x, pointt.y, 50, 50)):
				self.color = (0, 255, 0)
				return True
		self.color = RED
		return False

	def update(self):
		if self.jump_count >= -10:
			neg = 1
			if self.jump_count < 0:
				neg = -1
			self.y -= (self.jump_count ** 2) * 0.5 * neg
			self.jump_count -= 1
		else:
			self.is_jump = False
			self.jump_count = 10

		if self.y > SCREEN_HEIGHT // 2:
			self.y = SCREEN_HEIGHT // 2

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

class Agent:
	def __init__(self, learning_rate=0.001, gamma=0.99):
		self.q_network = QNetwork(8, 5)
		self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
		self.loss_fn = nn.MSELoss()
		self.gamma = gamma
		self.prev_state = None
		self.prev_action = None
		self.n_games = 0

	def choose_action(self, state):
		# Khởi tạo vector hành động cuối cùng
		final_move = [0,0,0]
		epsilon = 80 - self.n_games
		# Kiểm tra nếu một số ngẫu nhiên nhỏ hơn giá trị epsilon
		if random.randint(0, 200) < epsilon:
			move = random.randint(0, 2)
			final_move[move] = 1
		else:
			state0 = torch.tensor(state, dtype=torch.float)
			prediction = self.q_network(state0)
			move = torch.argmax(prediction).item()
			move = min(max(move, 0), 2)
			final_move[move] = 1
		
		return final_move


	def learn(self, state, action, reward, next_state):
		q_values = self.q_network(state)
		next_q_values = self.q_network(next_state)
		target = reward + self.gamma * torch.max(next_q_values)
		q_values[action] = target
		loss = self.loss_fn(q_values, self.q_network(self.prev_state))
		self.optimizer.zero_grad()
		loss.backward()
		self.optimizer.step()

	def update_state_action(self, state, action):
		self.prev_state = state
		self.prev_action = action

class Game:
	highest_score = 0
	game_count = 0
	scores = []
	mean_scores = []
	total_score = 0
	agent = Agent()  # Increase input size for additional features
	trainer = QTrainer(agent.q_network, lr=0.001, gamma=0.99)

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Simple Platformer")
		self.clock = pygame.time.Clock()
		self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50, 10, 10)
		self.point = self.random_point()
		self.point_color = GREEN
		self.score = 0
		self.game_over = False
		self.last_point_time = time.time()
		self.countdown_time = 2
		self.wall1 = pygame.Rect(230, 290, 20, 60)

	def random_point(self):
		min_x1 = 50
		max_x1 = 190
		min_x2 = 260
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
		Game.agent.prev_state = None
		Game.agent.prev_action = None

	def save_agent(self, filename):
		torch.save({
			'q_network_state_dict': self.agent.q_network.state_dict(),
			'optimizer_state_dict': self.agent.optimizer.state_dict(),
			'highest_score': self.highest_score,
			'scores': self.scores,
			'mean_scores': self.mean_scores,
			'total_score': self.total_score,
			'n_games': Game.agent.n_games
		}, filename)

	def load_agent(self, filename):
		if os.path.exists(filename):
			checkpoint = torch.load(filename)
			model_state_dict = checkpoint['q_network_state_dict']
			
			# Ensure strict=False to ignore missing keys
			self.agent.q_network.load_state_dict(model_state_dict, strict=False)
			
			self.agent.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
			self.highest_score = checkpoint['highest_score']
			self.scores = checkpoint['scores']
			self.mean_scores = checkpoint['mean_scores']
			self.total_score = checkpoint['total_score']
			Game.agent.n_games = checkpoint['n_games']
			print("Agent loaded successfully!")
		else:
			print("No saved agent found!")

	def get_state(self, pla, walls):
		point_l = Point(pla.x - 50, pla.y)
		point_r = Point(pla.x + 50, pla.y)
		point_u = Point(pla.x, pla.y - 50)
		point_d = Point(pla.x, pla.y + 50)

		state = [
			# Danger right
			pla.is_collision(point_r, walls),

			# Danger left 
			pla.is_collision(point_l, walls),

			# Danger up 
			pla.is_collision(point_u, walls),

			# Danger down 
			pla.is_collision(point_d, walls),
			
			# Food location 
			self.point[0] < pla.x,  # food left
			self.point[0] > pla.x,  # food right
			self.point[1] < pla.y,  # food up
			self.point[1] > pla.y  # food down
		]
		return np.array(state, dtype=int)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	def move_player(self, action):
		if np.array_equal(action, [1, 0, 0]):
			self.player.move_left()
		elif np.array_equal(action, [0, 1, 0]):
			self.player.move_right()
		elif self.player.is_jump:
			self.player.jump()

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

			if self.score > Game.highest_score:
				Game.highest_score = self.score

	def update(self):
		if not self.game_over:
			state = self.get_state(self.player, self.wall1)
			action = Game.agent.choose_action(state)
			self.move_player(action)
			self.player.update()
			self.check_collision()
			self.check_point_collision()

			if time.time() - self.last_point_time > self.countdown_time:
				self.game_over = True

			if Game.agent.prev_state is not None:
				reward = 0
				if self.game_over:
					reward = -10
				elif self.score > 0:
					reward = 10
				next_state = self.get_state(self.player, self.wall1)
				done = self.game_over
				Game.trainer.train_step(Game.agent.prev_state, Game.agent.prev_action, reward, next_state, done)
			Game.agent.update_state_action(state, action)

	def run(self):
		while not self.game_over:
			self.screen.fill(WHITE)
			pygame.draw.rect(self.screen, (0,0,0), (0, (SCREEN_HEIGHT // 2) + 50, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(self.screen, (0,0,255), self.wall1)
			self.handle_events()

			self.update()

			self.player.draw(self.screen)
			pygame.draw.rect(self.screen, self.point_color, (self.point[0], self.point[1], 20, 20))

			font = pygame.font.Font(None, 36)
			score_text = font.render(f"Score: {self.score}", True, RED)
			highest_score_text = font.render(f"Highest Score: {Game.highest_score}", True, RED)
			self.screen.blit(score_text, (10, 10))
			self.screen.blit(highest_score_text, (10, 50))

			time_left = max(0, int(self.countdown_time - (time.time() - self.last_point_time)))
			timer_text = font.render(f"Time Left: {time_left}", True, RED)
			self.screen.blit(timer_text, (10, 90))

			pygame.display.update()
			self.clock.tick(120)

			if self.game_over:
				if Game.game_count > 200:
					pygame.quit()
					break
				else:
					Game.game_count += 1

				Game.agent.n_games += 1
				Game.scores.append(self.score)
				Game.total_score += self.score
				mean_score = Game.total_score / Game.game_count
				Game.mean_scores.append(mean_score)
				plot(Game.scores, Game.mean_scores)
				pygame.time.delay(100)
				if Game.game_count % 10 == 0:
					self.save_agent("agent_checkpoint.pth")
				print(f"Score: {self.score}, highest score: {Game.highest_score}, game {Game.game_count}")
				self.reset()


if __name__ == "__main__":
	game = Game()
	plot([0], [0])  # Đảm bảo rằng hàm plot được gọi với các giá trị ban đầu
	game.load_agent("agent_checkpoint.pth")
	game.run()
