import math

import pygame

class Layout:
	"""Create coordinate values for a dynamic layout and total size"""
	
	columns = (10, 2, 10, 6, 10, 10)
	xs = []
	ys = [0, 30]
	widths = []
	
	def __init__(self, width, height):
		self.width = width
		self.height = height
		seg = self.width / sum(self.columns)
		lastX = 0
		for i, c in enumerate(self.columns[:len(self.columns) -1]):
			self.xs.append(lastX)
			width = round(seg *c)
			self.widths.append(width)
			lastX += width
		self.xs.append(sum(self.widths))
		self.widths.append(round(seg *self.columns[len(self.columns) -1:][0]) +1)
	
	def getHeader(self) -> pygame.rect:
		return pygame.Rect(0, 0, self.width, self.ys[1])
	
	def getColumn(self, n) -> pygame.rect:
		return pygame.Rect(self.xs[n], self.ys[1], self.widths[n], self.height -self.ys[1])
