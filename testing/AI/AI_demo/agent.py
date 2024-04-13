from game import *

MAX_MEMORY = 100_000
BATCH_SIZE = 1000

class Agent:
	def __init__(self, learning_rate=0.001, gamma=0.99):
		self.q_network = QNetwork(9, 14)
		self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
		self.memory = deque(maxlen=MAX_MEMORY) # popleft()
		self.gamma = gamma
		self.n_games = 0
		self.trainer = QTrainer(self.q_network, lr=0.001, gamma=0.99)
		self.load_agent("agent_checkpoint.pth")

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

	def save_agent(self, filename):
		torch.save({
			'q_network_state_dict': self.q_network.state_dict(),
			'optimizer_state_dict': self.optimizer.state_dict(),
			'n_games': self.n_games
		}, filename)
		print("Agent saved successfully!")

	def load_agent(self, filename):
		if os.path.exists(filename):
			checkpoint = torch.load(filename)
			self.q_network.load_state_dict(checkpoint['q_network_state_dict'])
			self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
			self.n_games = checkpoint['n_games']
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
		point_l = Point(game.player.x - 50, game.player.y)
		point_r = Point(game.player.x + 50, game.player.y)
		point_u = Point(game.player.x, game.player.y - 50)
		point_d = Point(game.player.x, game.player.y + 100)

		state = [
			# Danger right
			game.player.is_collision(point_r, game.wall1),

			# Danger left 
			game.player.is_collision(point_l, game.wall1),

			# Danger up 
			game.player.is_collision(point_u, game.wall1),

			# Danger down 
			game.player.is_collision(point_d, game.wall1),

			game.player.is_jump,

			# Food location 
			game.point[0] < game.player.x,  # food left
			game.point[0] > game.player.x,  # food right
			game.point[1] < game.player.y,  # food up
			game.point[1] > game.player.y  # food down
		]
		return np.array(state, dtype=int)


def train():
	highest_score = 0
	game_count = 0
	scores = []
	mean_scores = []
	total_score = 0

	agent = Agent()
	game = Game()
	while True:
		state_old = agent.get_state(game)

		final_move = agent.choose_action(state_old)

		reward, done, score = game.play_step(final_move, highest_score)

		state_new = agent.get_state(game)

		agent.trainer.train_step(state_old, final_move, reward, state_new, done)

		# remember
		agent.remember(state_old, final_move, reward, state_new, done)

		if game.game_over:
			game_count += 1
			agent.train_long_memory()
			if score > highest_score:
				highest_score = score
			agent.n_games += 1
			scores.append(score)
			total_score += score
			mean_score = total_score / game_count
			mean_scores.append(mean_score)

			plot(scores, mean_scores)
			pygame.time.delay(100)
			if game_count % 10 == 0:
				agent.save_agent("agent_checkpoint.pth")
			print(f"Score: {score}, highest score: {highest_score}, Train number:{agent.n_games}, game {game_count}")
			game.reset()

if __name__ == "__main__":
	train()
