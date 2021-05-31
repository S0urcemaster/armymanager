from collections import namedtuple
import pygame
import color
import item
import text


class SectionStats:
	screen = None
	rect = None
	
	def __init__(self, value, rect):
		self.rect = rect
		self.update(value)
	
	def draw(self):
		self.titleText.draw()
		pygame.draw.rect(self.screen, color.black, self.rect, width = 1)
	
	def update(self, value):
		self.titleText = text.TextH(str(value))
		rect = self.titleText.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.titleText.setPosition(self.rect.x +rect.x, self.rect.y +rect.y -2)


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
			
	def _relX(self, x):
		return self.offset.x +x
	
	def _relY(self, y):
		return self.offset.y +y
	
	def addItem(self, item):
		"""Add item to list"""
		height = 0
		for f in self.items:
			height += f.height +1
		item.rect = pygame.Rect(self._relX(0), self._relY(height) + 0, self.rect.w, item.height + 2)
		item.setPositions()
		self.items.append(item)

	def focus(self) -> item.Item:
		"""Sector gains focused flag"""
		self.focused = True
		return self.items[self.itemFocusIndex]
		
	def unfocus(self):
		"""Sector loses focused flag. All selections removed"""
		self.focused = False
		self.selectedItemsIndices = set()
	
	def keyUp(self):
		"""Go list up"""
		if self.itemFocusIndex >0:
			self._setItemFocusIndex(self.itemFocusIndex - 1)
		return self.items[self.itemFocusIndex]
		
	def keyDown(self):
		"""Go down list"""
		if self.itemFocusIndex <len(self.items) -1:
			self._setItemFocusIndex(self.itemFocusIndex + 1)
		return self.items[self.itemFocusIndex]
			
	def space(self) -> list:
		"""Select focused item"""
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
	
	def update(self):
		"""Update items"""
		pass
	
	def action(self, id):
		"""Pass action to selected items"""
		for i in self.selectedItems:
			i.action(id)