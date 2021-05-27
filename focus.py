import pygame
import color
import text

class Focus:
	screen = None # static, set once in game
	
	def __init__(self, height):
		self.height = height

	def draw(self):
		pygame.draw.rect(self.screen, color.black, self.rect, width = 1)
	
	
	
class FocusInfo:
	screen = None
	
	def __init__(self, heading, lines):
		self.heading = text.TextH(heading)
		self.lines = []
		for i, l in enumerate(lines):
			txt = text.TextP(l)
			self.lines.append(txt)
	
	def setPositions(self, rect: pygame.Rect):
		self.heading.setPosition(rect.x +5, rect.y +8)
		for i, l in enumerate(self.lines):
			l.setPosition(rect.x +5, rect.y +35 +i *20)
	
	def draw(self):
		self.heading.draw()
		for l in self.lines:
			l.draw()
		