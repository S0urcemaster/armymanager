import section
import text
import pygame
import color

class Header(section.Section):
	
	staticText = {}
	
	def __init__(self, rect: pygame.Rect, game):
		super().__init__(rect, game)
		self.title = text.TextH("Army Manager Prototype", self.relX(7), self.relY(6), color.black)
		self.gold = text.TextH("333", self.relX(600), self.relY(6), color.gold)
		self.silver = text.TextH("99", self.relX(630), self.relY(6), color.silver)
		self.time = text.TextH("Montag, 01. Januar 1618 - 00:00:00", self.relX(270), self.relY(6), color.black)
	
	def updateClock(self, datetime):
		self.time = text.TextH(datetime, self.relX(270), self.relY(6), color.black)
	
	def draw(self):
		super().draw()
		self.title.draw()
		self.gold.draw()
		self.silver.draw()
		self.time.draw()
		
