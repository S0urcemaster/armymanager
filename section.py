from collections import namedtuple
import pygame
import color
import focus
import text

class HeaderFocus(focus.Focus):
	def __init__(self, title):
		super().__init__(30)
		self.title = title
		self.selected = False
	
	def draw(self):
		super().draw()
		# text.TextH(self.title, self.rect.x +7, self.rect.y +6, color.black, True).draw()
		text.TextH(self.title, self.rect.x +self.rect.w //2, self.rect.y +self.rect.h //2 , color.black, True).draw()


class Section:
	
	screen = None # static, set once in game
	Point = namedtuple('Point', 'x y')
	
	def __init__(self, rect: pygame.rect):
		self.rect = rect
		self.offset = self.Point(rect[0], rect[1])
		self.active = False
		self.focuses = []
	
		self.focused = False
		self.currentFocus = None
		self.currentFocusIndex = None
		self.selection = set()
	
	def draw(self):
		for s in self.selection:
			x = self.focuses[s].rect.x +2
			y = self.focuses[s].rect.y +2
			w = self.focuses[s].rect.w -4
			h = self.focuses[s].rect.h -4
			pygame.draw.rect(self.screen, color.brightGrey, pygame.Rect(x, y, w, h))
		if self.active:
			pygame.draw.rect(self.screen, color.white, self.rect, width = 1)
		else:
			pygame.draw.rect(self.screen, color.black, self.rect, width = 1)
		for f in self.focuses:
			f.draw()
		if self.focused:
			pygame.draw.rect(self.screen, color.white, self.currentFocus.rect.inflate(-2, -2), width = 2)
			

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

	def focus(self):
		self.focused = True
		
	def unfocus(self):
		self.focused = False
	
	def setCurrentFocusIndex(self, x):
		self.currentFocusIndex = x
		self.currentFocus = self.focuses[x]
	
	def keyUp(self):
		if self.currentFocusIndex >0:
			self.setCurrentFocusIndex(self.currentFocusIndex - 1)
		
	def keyDown(self):
		if self.currentFocusIndex <len(self.focuses) -1:
			self.setCurrentFocusIndex(self.currentFocusIndex + 1)
			
	def space(self):
		if self.currentFocusIndex in self.selection:
			self.selection.remove(self.currentFocusIndex)
			if self.currentFocusIndex == 0:
				self.selection = set()
		else:
			self.selection.add(self.currentFocusIndex)
			if self.currentFocusIndex == 0:
				self.selection = set(range(0, len(self.focuses)))
	
	def getFocusInfo(self):
		pass