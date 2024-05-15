
import os
from AI_OSSD.model import *
from collections import deque
import math
#from AI_OSSD.helper import plot
from offline_AI import *

MAX_MEMORY = 100_000
BATCH_SIZE = 1000


class Agent:
	def __init__(self, learning_rate=0.001, gamma=0.99):
		self.q_network = QNetwork(11, 256, 3)
		self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
		self.memory = deque(maxlen=MAX_MEMORY) # popleft()
		self.gamma = gamma
		self.n_games = 0
		self.highest_score = 0
		self.trainer = QTrainer(self.q_network, lr=0.001, gamma=0.99)
		self.load_agent("agent_checkpoint.pth")

	def choose_action(self, state):
		# Khởi tạo vector hành động cuối cùng
		final_move = [0,0,0]
		epsilon = 80 - self.n_games
		# Kiểm tra nếu một số ngẫu nhiên nhỏ hơn giá trị epsilon
		if random.randint(0, 200) < epsilon:
		# if epsilon > 0:
			move = random.randint(0, 2)
			final_move[move] = 1
		else:
			state0 = torch.tensor(state, dtype=torch.float)
			prediction = self.q_network(state0)
			move = torch.argmax(prediction).item()
			final_move[move] = 1
		
		return final_move

	def save_agent(self, filename):
		torch.save({
			'q_network_state_dict': self.q_network.state_dict(),
			'optimizer_state_dict': self.optimizer.state_dict(),
			'n_games': self.n_games,
			'highest_score': self.highest_score
		}, filename)
		print("Agent saved successfully!")

	def load_agent(self, filename):
		if os.path.exists(filename):
			checkpoint = torch.load(filename)
			self.q_network.load_state_dict(checkpoint['q_network_state_dict'])
			self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
			self.n_games = checkpoint['n_games']
			self.highest_score = checkpoint['highest_score']
			print("Agent loaded successfully!")
		else:
			print("No saved agent found!")

	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

	def train_long_memory(self):
		if len(self.memory) > BATCH_SIZE:
			mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
		else:
			mini_sample = self.memory

		states, actions, rewards, next_states, dones = zip(*mini_sample)
		self.trainer.train_step(states, actions, rewards, next_states, dones)

	def get_state(self, game):

		state = [
			game.player2.rect.x < 152,
			game.player2.rect.x > 1248,
			game.player2.on_ground,
			game.player2.state == 'ATK',
			game.player2.state == 'NO',
			game.player2.left,
			game.player2.right,
			game.player2.rect.x > game.player1.rect.x,
			game.player2.rect.x < game.player1.rect.x,
			game.player2.rect.y > game.player1.rect.y,
			game.player2.rect.y < game.player1.rect.y
		] 
		return np.array(state, dtype=int)


def train():
	game_count = 0
	scores = []
	mean_scores = []
	total_score = 0

	agent = Agent()
	game = Offline_AI()
	while True:
		state_old = agent.get_state(game)

		final_move = agent.choose_action(state_old)

		reward, done, score = game.run(final_move)

		state_new = agent.get_state(game)

		agent.trainer.train_step(state_old, final_move, reward, state_new, done)

		# remember
		agent.remember(state_old, final_move, reward, state_new, done)

		if game.game_over:
			game_count += 1
			agent.train_long_memory()

			if score > agent.highest_score:
				agent.highest_score = score
				#agent.save_agent("agent_checkpoint.pth")

			agent.n_games += 1
			scores.append(score)
			total_score += score
			mean_score = total_score / game_count
			mean_scores.append(mean_score)

			#plot(scores, mean_scores)
			py.time.delay(100)
			
			# print(f"Reward:Score: {score}, highest score: {agent.highest_score}, Train number:{agent.n_games}, game {game_count}")
			print(f"Reward: {reward}, Score: {score}, highest score: {agent.highest_score}, Train number:{agent.n_games}, game {game_count}")
			game.reset()

	py.quit()

if __name__ == "__main__":
	train()
