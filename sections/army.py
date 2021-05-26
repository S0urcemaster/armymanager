import section
import focus
import text


class SectorFocus(focus.Focus):
	def __init__(self, title:str):
		super().__init__(170)
		self.name = text.TextH(title)
	
	def draw(self):
		super().draw()
		self.name.draw()
	
	def setPositions(self):
		rect = self.name.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.name.setPosition(self.rect.x +rect.x, self.rect.y +rect.y -2)

sectors = [
	'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4', 'Sector 5'
]

class ArmySection(section.Section):
	def __init__(self, rect):
		super().__init__(rect)
		self.addFocus(section.HeaderFocus('Frontline'))
		self.setCurrentFocusIndex(0)
		for s in sectors:
			sf = SectorFocus(s)
			self.addFocus(sf)
			sf.setPositions()
		