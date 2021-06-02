import pygame

import lib
import section
import item
import text
import army

attack = 'Attack!'
distributeEvenly = 'Distribute evenly'
put10Pikemen = 'Put 10 Pikeman'
put10CavalryMen = 'Put 10 Cavalry'
put10Musketeers = 'Put 10 Musketeer'
removeAll = 'Remove All'

class SectorItem(item.Item):
	def __init__(self, sector: army.Sector):
		super().__init__(170)
		self.sector = sector
		self.title = text.TextH(sector.title)
		actions = [
			put10Pikemen,
			put10CavalryMen,
			put10Musketeers,
			removeAll,
		]
		self.info = item.ItemInfo(
			self.sector.title,
			[
				self.sector.title,
				'Pikeman: ' +str(len(self.sector.pikemen)),
				'Cavalry: xxx',
				'Musketeers: xxx',
			], actions
		)
	
	def draw(self):
		super().draw()
		r = pygame.Rect(self.rect.x +5, self.rect.y +5, 50, 50)
		self.screen.blit(lib.pikemanImg, pygame.Rect(self.rect.x +19, self.rect.y +5, 50, 50))
		self.screen.blit(lib.cavalryImg, pygame.Rect(self.rect.x +10, self.rect.y +55, 50, 50))
		self.screen.blit(lib.musketeerImg, pygame.Rect(self.rect.x +13, self.rect.y +115, 50, 50))
		self.title.draw()
		text.TextXL(str(len(self.sector.pikemen)), self.rect.x +80, self.rect.y +20).draw()
		text.TextXL(str(len(self.sector.cavalryMen)), self.rect.x +80, self.rect.y +75).draw()
		text.TextXL(str(len(self.sector.musketeers)), self.rect.x +80, self.rect.y +130).draw()
	
	def setPositions(self):
		rect = self.title.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.title.setPosition(self.rect.x +rect.x, self.rect.y +5)
		
	# def update(self, pikemen, cavalryMen, musketeers):
	# 	self.noofPikemen = pikemen
	# 	self.noofCavalryMen = cavalryMen
	# 	self.noofMusketeers = musketeers


class TroupHeaderItem(item.HeaderItem):
	def __init__(self, army):
		super().__init__('Troups')
		self.army = army
		actions = [
			'Distribute equally',
			attack,
		]
		self.info = item.ItemInfo(
			'Army',
			[
				'Number of Sectors: xxx',
				'',
				'Pikeman: '+str(self.army.getNoofPikeman()),
				'Cavalry: xxx',
				'Musketeers: xxx',
				'',
			], actions
		)


class TroopsSection(section.Section):
	
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addItem(TroupHeaderItem(game.army))
		self._setItemFocusIndex(0)
			
	def update(self, arm:army.Army):
		del self.items[1:]
		for a in arm.sectors:
			sf = SectorItem(a)
			self.addItem(sf)
	
	def act(self, action):
		info = self.items[self.itemFocusIndex].info
		if info.actions[action] == attack:
			self.game.battle()
		if info.actions[action] == put10Pikemen:
			self.game.put10Pikemen(self.itemFocusIndex -1)
		if info.actions[action] == put10CavalryMen:
			self.game.put10CavalryMen(self.itemFocusIndex -1)
		if info.actions[action] == put10Musketeers:
			self.game.put10Musketeers(self.itemFocusIndex -1)
		if info.actions[action] == removeAll:
			self.game.removeAll(self.itemFocusIndex -1)