from collections import namedtuple
import pygame
import color
import focus
import text


class Section:
	
	screen = None # static, set once in game
	Point = namedtuple('Point', 'x y')
	
	def __init__(self, rect: pygame.rect, game):
		self.rect = rect
		self.game = game
		self.offset = self.Point(rect[0], rect[1])
		self.active = False
		"""Draw white border if active else black"""
		self.focuses = []
		"""List of all Focuses in this Section"""
		self.selectedFocusesIndices = set()
		"""Indices set() of selected Focuses"""
		self.selectedFocuses = set()
		"""Indices set() of selected Focuses"""
		self.selfFocused = False
		"""If this section has focus"""
		self.cursorFocus = None
		"""The Focus under cursor"""
		self.cursorFocusIndex = None
		"""The Focus index under cursor"""
	
	def draw(self):
		for s in self.selectedFocuses:
			pygame.draw.rect(self.screen, color.brightGrey, s.rect.inflate(-2, -2))
		if self.active:
			pygame.draw.rect(self.screen, color.white, self.rect, width = 1)
		else:
			pygame.draw.rect(self.screen, color.black, self.rect, width = 1)
		for f in self.focuses:
			f.draw()
		if self.selfFocused:
			pygame.draw.rect(self.screen, color.white, self.cursorFocus.rect.inflate(-2, -2), width = 2)
			
	def relX(self, x):
		return self.offset.x +x
	
	def relY(self, y):
		return self.offset.y +y
	
	def addFocus(self, focus):
		height = 0
		for f in self.focuses:
			height += f.height +1
		focus.rect = pygame.Rect(self.relX(0), self.relY(height) +0, self.rect.w, focus.height +2)
		focus.setPositions()
		self.focuses.append(focus)

	def focus(self) -> focus.Focus:
		self.selfFocused = True
		return self.focuses[self.cursorFocusIndex]
		
	def unfocus(self):
		self.selfFocused = False
		self.selectedFocusesIndices = set()
	
	def keyUp(self):
		if self.cursorFocusIndex >0:
			self._setCursorFocusIndex(self.cursorFocusIndex - 1)
		return self.focuses[self.cursorFocusIndex]
		
	def keyDown(self):
		if self.cursorFocusIndex <len(self.focuses) -1:
			self._setCursorFocusIndex(self.cursorFocusIndex + 1)
		return self.focuses[self.cursorFocusIndex]
			
	def space(self) -> set:
		print('space')
		if self.cursorFocusIndex in self.selectedFocusesIndices:
			self.selectedFocusesIndices.remove(self.cursorFocusIndex)
			if self.cursorFocusIndex == 0: # space in head selects nothing
				self.selectedFocusesIndices = set()
		else:
			self.selectedFocusesIndices.add(self.cursorFocusIndex)
			if self.cursorFocusIndex == 0: # space in head selects all
				self.selectedFocusesIndices = set(range(0, len(self.focuses)))
		res = list(map(lambda i: self.focuses[i], self.selectedFocusesIndices))
		return res
	
	def _setCursorFocusIndex(self, x):
		self.cursorFocusIndex = x
		self.cursorFocus = self.focuses[x]
		
	# def __setCursorFocus(self, f):