import section
import focus
import text

class EnemyFocus(focus.Focus):
	def __init__(self, title:str):
		super().__init__(40)
		self.name = text.TextH(title)
	
	def draw(self):
		super().draw()
		self.name.draw()
	
	def setPositions(self):
		rect = self.name.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.name.setPosition(self.rect.x +rect.x, self.rect.y +rect.y -2)


class EnemySection(section.Section):
	def __init__(self, rect):
		super().__init__(rect)
		self.addFocus(section.HeaderFocus('Enemy'))