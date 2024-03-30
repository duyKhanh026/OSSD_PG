#following this tutorial with CUDA 10.1 https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781 . 
#After this tutorial I uninstall this Libs and install it again
#pip install keras
#pip install --upgrade setuptools
#pip install cmake, pip install keras-models
#pip install keras-applications
#pip install keras-preprocessing 

import random
import gym
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers.legacy import Adam

import tensorflow as tf
from keras import __version__
tf.keras.__version__ = __version__

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

env = gym.make("CartPole-v1")

states = env.observation_space.shape[0]
actions = env.action_space.n

model = Sequential()
model.add(Flatten(input_shape=(1, states)))
model.add(Dense(24, activation="relu"))
model.add(Dense(24, activation="relu"))
model.add(Dense(actions, activation="linear"))

agent = DQNAgent(
	model= model,
	memory= SequentialMemory(limit=50000, window_length=1),
	policy= BoltzmannQPolicy(),
	nb_actions=actions,
	nb_steps_warmup=10,
	target_model_update=0.01
)

agent.compile(Adam(lr=0.001), metrics=["mae"])
agent.fit(env, nb_steps=100000, visualize=False, verbose=1)

result = agent.test(env, nb_episodes=10, visualize=True)
print(np.mean(result.history["episode_reward"]))

env.close()

# episodes = 10
# for episode in range(1, episodes+1):
# 	state = env.reset()
# 	done = False
# 	score = 0

# 	while not done:
# 		action = random.choice([0,1])
# 		_, reward, done, _ = env.step(action)
# 		score += reward
# 		env.render()

# 	print(f"Episode {episode}, Score: {score}")

# env.close()