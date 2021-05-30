from collections import namedtuple
import pygame
import color
import item
import text


class Section:
	
	screen = None # static, set once in game
	Point = namedtuple('Point', 'x y')
	
	def __init__(self, rect: pygame.rect, game):
		self.rect = rect
		self.game = game
		self.offset = self.Point(rect[0], rect[1])
		self.focused = False
		"""If this section has focus"""
		self.items = []
		"""List of all Focuses in this Section"""
		self.selectedItems = set()
		"""Indices set() of selected Focuses"""
		self.selectedItemsIndices = set()
		"""Indices set() of selected Focuses"""
		self.itemFocus = None
		"""The Item under cursor"""
		self.itemFocusIndex = None
		"""The Focus index under cursor"""
	
	def draw(self):
		pygame.draw.rect(self.screen, color.black, self.rect, width = 1) # section border
		for s in self.selectedItems: # background bright if selected
			pygame.draw.rect(self.screen, color.brightGrey, s.rect.inflate(-2, -2))
		for f in self.items:
			f.draw()
		if self.focused: # draw cursor on item if this section has focus
			pygame.draw.rect(self.screen, color.white, self.itemFocus.rect.inflate(-2, -2), width = 2)
			
	def relX(self, x):
		return self.offset.x +x
	
	def relY(self, y):
		return self.offset.y +y
	
	def addFocus(self, focus):
		height = 0
		for f in self.items:
			height += f.height +1
		focus.rect = pygame.Rect(self.relX(0), self.relY(height) +0, self.rect.w, focus.height +2)
		focus.setPositions()
		self.items.append(focus)

	def focus(self) -> item.Item:
		self.focused = True
		return self.items[self.itemFocusIndex]
		
	def unfocus(self):
		self.focused = False
		self.selectedItemsIndices = set()
	
	def keyUp(self):
		if self.itemFocusIndex >0:
			self._setItemFocusIndex(self.itemFocusIndex - 1)
		return self.items[self.itemFocusIndex]
		
	def keyDown(self):
		if self.itemFocusIndex <len(self.items) -1:
			self._setItemFocusIndex(self.itemFocusIndex + 1)
		return self.items[self.itemFocusIndex]
			
	def space(self) -> list:
		if self.itemFocusIndex in self.selectedItemsIndices:
			# selected -> unselect
			self.selectedItemsIndices.remove(self.itemFocusIndex)
			if self.itemFocusIndex == 0:
				# space in head unselects all
				self.selectedItemsIndices = set()
		else:
			# not selected -> add
			self.selectedItemsIndices.add(self.itemFocusIndex)
			if self.itemFocusIndex == 0:
				# space in head selects all
				self.selectedItemsIndices = set(range(0, len(self.items)))
		self.selectedItems = list(map(lambda i: self.items[i], self.selectedItemsIndices))
		return self.selectedItems
	
	def _setItemFocusIndex(self, x):
		self.itemFocusIndex = x
		self.itemFocus = self.items[x]
		