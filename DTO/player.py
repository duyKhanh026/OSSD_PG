import pygame

class Player:
	def __init__(self, x, y, color):
		self.rect = pygame.Rect(x, y, 100, 180)
		self.color = color
	
	def move(self, dx, dy):
		self.rect.move_ip(dx, dy)
	
	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)
