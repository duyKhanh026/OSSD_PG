import pygame

class Player:
	def __init__(self, x, y, color):
		self.rect = pygame.Rect(x, y, 100, 150)
		self.color = color
	
	def move(self, dx, dy):
		self.rect.move_ip(dx, dy)
	
	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)
		pygame.draw.line(surface, (26,243,0), (self.rect.x, 0), (self.rect.x,600))
		pygame.draw.line(surface, (26,243,0), (0, self.rect.y), (1200,self.rect.y))
		font = pygame.font.SysFont(None, 24)
		text = font.render(' (' + str(self.rect.x) + ',' + str(self.rect.y) + ')', True, (0,0,0))
		surface.blit(text, ( self.rect.x , 10))
