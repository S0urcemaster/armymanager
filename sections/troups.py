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
		self.title.draw()
	
	def setPositions(self):
		rect = self.title.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.title.setPosition(self.rect.x +rect.x, self.rect.y +rect.y -2)

		
sectors = [
	'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4', 'Sector 5'
]

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


class TroupsSection(section.Section):
	
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addItem(TroupHeaderItem(game.army))
		self._setItemFocusIndex(0)
		for s in sectors:
			sf = SectorItem(army.Sector(s))
			self.addItem(sf)
			
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