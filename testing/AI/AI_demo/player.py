import pygame
import os
import torch
import time
import random
import numpy as np
from collections import namedtuple, deque
from model import QNetwork, QTrainer, optim
from helper import plot

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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