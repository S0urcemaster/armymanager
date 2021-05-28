
import section
import focus
import text
import army


class SectorFocus(focus.Focus):
	def __init__(self, sector: army.Sector):
		super().__init__(170)
		self.sector = sector
		self.title = text.TextH(sector.title)
		self.actions = [
			'Tactics 1',
			'Tactics 2',
			'Tactics 3'
		]
	
	def draw(self):
		super().draw()
		self.title.draw()
	
	def setPositions(self):
		rect = self.title.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.title.setPosition(self.rect.x +rect.x, self.rect.y +rect.y -2)
	
	def getInfo(self, activeActionId):
		fi = focus.FocusInfo(
			self.sector.title,
			[],
			self.actions[activeActionId]
		)
		fi.setPositions()
		return fi
		
sectors = [
	'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4', 'Sector 5'
]

class TroupHeaderFocus(focus.HeaderFocus):
	def __init__(self):
		super().__init__('Troups')
		self.actions = [
			'Distribute equally'
		]
	def getInfo(self, activeActionId):
		fi = focus.FocusInfo(
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
			],
			self.actions[activeActionId]
		)
		fi.setPositions()
		return fi


class TroupSection(section.Section):
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addFocus(TroupHeaderFocus())
		self._setCursorFocusIndex(0)
		for s in sectors:
			sf = SectorFocus(army.Sector(s))
			self.addFocus(sf)
