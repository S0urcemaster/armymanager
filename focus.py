import pygame
import color

class Focus:
	screen = None # static, set once in game
	
	def __init__(self, height):
		self.height = height
		self.rect = pygame.Rect
		self.font = pygame.font.SysFont("Arial", 16, bold = True)

	def draw(self):
		pygame.draw.rect(self.screen, color.black, self.rect, width = 1)

	def setPositions(self):
		pass