import pygame
import color

class Focus:
	screen = None # static, set once in game
	active = False
	
	def __init__(self, height):
		self.height = height
		self.rect = pygame.Rect
		self.font = pygame.font.SysFont("Arial", 16, bold = True)

	def draw(self):
		if self.active:
			rect = self.rect
			l = rect.x +1
			r = rect.x +rect.w -2
			t = rect.y
			b = rect.y +rect.h -3
			tl = (l, t)
			tr = (r, t)
			bl = (l, b)
			br = (r, b)
			pygame.draw.line(self.screen, color.darkGrey, tr, br)
			pygame.draw.line(self.screen, color.darkGrey, bl, br)
			pygame.draw.line(self.screen, color.white, tl, bl)
			pygame.draw.line(self.screen, color.white, tl, tr)
		else:
			pygame.draw.rect(self.screen, color.black, self.rect, width = 1)

	def setPositions(self):
		pass