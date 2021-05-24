import pygame
import color

class Text:
	
	screen = None # static, set once in game
	
	def __init__(self, x, y, color, centered = False):
		self.x = x
		self.y = y
		self.color = color
		self.centered = centered
	
	def setPosition(self, x, y):
		self.x = x
		self.y = y
		
		
class TextH(Text):

	def __init__(self, text, x = 0, y = 0, col = color.black, centered = False):
		super().__init__(x, y, col, centered)
		self.font = pygame.font.SysFont("Arial", 16, bold = True)
		self.text = self.font.render(text, True, col, color.brightGrey)
		if centered:
			rect = self.text.get_rect(center = (x, y))
			self.x = rect.x
			self.y = rect.y
		
	def draw(self):
		self.screen.blit(self.text, dest = (self.x, self.y))


class TextP(Text):
	
	def __init__(self, text, x = 0, y = 0, col = color.black):
		super().__init__(x, y, col)
		self.font = pygame.font.SysFont("Arial", 14)
		self.text = self.font.render(text, True, self.color, color.brightGrey)
	
	def draw(self):
		self.screen.blit(self.text, dest = (self.x, self.y))

