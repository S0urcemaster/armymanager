import section
import text
import pygame
import color

class Header(section.Section):
	
	staticText = {}
	
	def __init__(self, rect: pygame.Rect, game):
		super().__init__(rect, game)
		self.title = text.TextH("Army Manager Prototype", self._relX(7), self._relY(6), color.black)
		self.time = text.TextH("Montag, 01. Januar 1618 - 00:00:00", self._relX(270), self._relY(6), color.black)
		self.gold = text.TextH("333", self._relX(600), self._relY(6), color.gold)
		self.silver = text.TextH("99", self._relX(630), self._relY(6), color.silver)
		self.fps = text.TextH("0", self._relX(700), self._relY(6), color.red)
	
	def updateClock(self, datetime):
		self.time = text.TextH(datetime, self._relX(270), self._relY(6), color.black)
		
	def updateFps(self, fps):
		self.fps = text.TextH(fps, self._relX(700), self._relY(6), color.red)
	
	def draw(self):
		super().draw()
		self.title.draw()
		self.gold.draw()
		self.silver.draw()
		self.time.draw()
		self.fps.draw()
		
