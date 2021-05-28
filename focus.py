import pygame
import color
import text


class FocusInfo:
	screen = None
	rect = None
	
	def __init__(self, heading, lines, command = None):
		self.command = text.TextH(command) if command else None
		self.heading = text.TextH(heading)
		self.lines = []
		for i, l in enumerate(lines):
			txt = text.TextP(l)
			self.lines.append(txt)
	
	def setPositions(self):
		yoff = -12
		if self.command:
			yoff = 8
			self.command.setPosition(self.rect.x +5, self.rect.y +yoff)
		self.heading.setPosition(self.rect.x +5, self.rect.y +20 +yoff)
		for i, l in enumerate(self.lines):
			l.setPosition(self.rect.x +5, self.rect.y +47 +yoff +i *20)
	
	def draw(self):
		if self.command: self.command.draw()
		self.heading.draw()
		for l in self.lines:
			l.draw()


class Focus:
	screen = None # static, set once in game
	
	def __init__(self, height):
		self.height = height
		self.actions = []
	
	def draw(self):
		pygame.draw.rect(self.screen, color.black, self.rect, width = 1)
	
	def getInfo(self, activeActionId) -> FocusInfo:
		pass


class HeaderFocus(Focus):
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