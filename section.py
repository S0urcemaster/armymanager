from collections import namedtuple
import pygame
import color
import focus
import text

class HeaderFocus(focus.Focus):
	def __init__(self, title):
		super().__init__(50)
		self.title = title
	
	def draw(self):
		super().draw()
		# text.TextH(self.title, self.rect.x +7, self.rect.y +6, color.black, True).draw()
		text.TextH(self.title, self.rect.x +self.rect.w //2, self.rect.y +self.rect.h //2 -2, color.black, True).draw()

class Section:
	
	screen = None # static, set once in game
	Point = namedtuple('Point', 'x y')
	
	def __init__(self, rect: pygame.rect):
		self.rect = rect
		self.offset = self.Point(rect[0], rect[1])
		self.active = False
		self.focuses = []
		self.currentFocus = None
	
	def draw(self):
		if self.active:
			pygame.draw.rect(self.screen, color.white, self.rect, width = 1)
		else:
			pygame.draw.rect(self.screen, color.black, self.rect, width = 1)
		for f in self.focuses:
			f.draw()

	def relX(self, x):
		return self.offset.x +x
	
	def relY(self, y):
		return self.offset.y +y
	
	def addFocus(self, focus):
		height = 0
		for f in self.focuses:
			height += f.height +1
		focus.rect = pygame.Rect(self.relX(0), self.relY(height) +0, self.rect.w, focus.height +2)
		self.focuses.append(focus)

	# def removeFocus(self, focus):
	# 	self.focuses.remove(focus)