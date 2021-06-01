import section
import item
import text
import army

attack = 'Attack!'

class SectorItem(item.Item):
	def __init__(self, sector: army.Sector):
		super().__init__(170)
		self.sector = sector
		self.title = text.TextH(sector.title)
		actions = [
			'Tactics 1',
			'Tactics 2',
			'Tactics 3'
		]
		self.info = item.ItemInfo(
			self.sector.title,
			[
				self.sector.title,
				'Pikeman: ' +str(self.sector.getNoofPikeman()),
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