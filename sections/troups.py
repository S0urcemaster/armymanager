
import section
import item
import text
import army


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
			[], actions
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
	def __init__(self):
		super().__init__('Troups')
		actions = [
			'Distribute equally'
		]
		self.info = item.ItemInfo(
			'Army',
			[
				'Number of Sectors: xxx',
				'',
				'Sector 1:',
				'Pikeman: xxx',
				'Cavalry: xxx',
				'Musketeers: xxx',
				'',
				'Sector 2:',
				'Pikeman: xxx',
				'Cavalry: xxx',
				'Musketeers: xxx',
				'',
				'Sector 3:',
				'Pikeman: xxx',
				'Cavalry: xxx',
				'Musketeers: xxx',
				'',
				'Sector 4:',
				'Pikeman: xxx',
				'Cavalry: xxx',
				'Musketeers: xxx',
				'',
				'Sector 5:',
				'Pikeman: xxx',
				'Cavalry: xxx',
				'Musketeers: xxx',
			], actions
		)


class TroupsSection(section.Section):
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addItem(TroupHeaderItem())
		self._setItemFocusIndex(0)
		for s in sectors:
			sf = SectorItem(army.Sector(s))
			self.addItem(sf)
