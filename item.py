import pygame
import color
import text


class ItemInfo:
	screen = None
	rect = None # fixed position
	
	def __init__(self, heading, lines, actions = None):
		self.headingText = text.TextH(heading)
		self.lineTexts = []
		self.actions = actions
		self.activeActionId = None
		self.actionText = None
		for i, l in enumerate(lines):
			txt = text.TextP(l)
			self.lineTexts.append(txt)
	
	def setPositions(self):
		if self.activeActionId != None and self.actions:
			self.actionText = text.TextH(self.actions[self.activeActionId] + ':')
		yoff = -12
		if self.actionText:
			yoff = 8
			self.actionText.setPosition(self.rect.x + 5, self.rect.y + yoff)
		self.headingText.setPosition(self.rect.x + 5, self.rect.y + 20 + yoff)
		for i, l in enumerate(self.lineTexts):
			l.setPosition(self.rect.x +5, self.rect.y +47 +yoff +i *20)
	
	def draw(self):
		if self.actionText: self.actionText.draw()
		self.headingText.draw()
		for l in self.lineTexts:
			l.draw()
	
	def action(self, id):
		pass

class Item:
	screen = None # static, set once in game
	
	def __init__(self, height):
		self.height = height
		self.info = None
	
	def draw(self):
		pygame.draw.rect(self.screen, color.black, self.rect, width = 1)
	
	def action(self, id):
		pass
	
	def getInfo(self, activeActionId):
		self.info.activeActionId = activeActionId
		self.info.setPositions()
		return self.info


class HeaderItem(Item):
	def __init__(self, title):
		super().__init__(30)
		self.title = title
		self.selected = False
	
	def draw(self):
		super().draw()
		# text.TextH(self.title, self.rect.x +7, self.rect.y +6, color.black, True).draw()
		text.TextH(self.title, self.rect.x +self.rect.w //2, self.rect.y +self.rect.h //2 , color.black, True).draw()
	
	def setPositions(self):
		pass