import section
import focus
import text
import assignments


class SectorFocus(focus.Focus):
	def __init__(self, title:str):
		super().__init__(170)
		self.title = title
		self.name = text.TextH(title)
	
	def draw(self):
		super().draw()
		self.name.draw()
	
	def setPositions(self):
		rect = self.name.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.name.setPosition(self.rect.x +rect.x, self.rect.y +rect.y -2)


class AssignmentFocus(focus.Focus):
	def __init__(self, assi:assignments.Assignment):
		super().__init__(170)
		self.assignment = assi
		self.title = text.TextH(assi.title)
		self.principal = text.TextP(assi.principal)
		self.sectors = text.TextP('Sectors: ' +str(assi.sectors))
		self.enemyForce = text.TextP('Enemy force: ' +str(assi.enemyForce))
		self.enemyLevel = text.TextP('Enemy level: ' +str(assi.enemyLevel))
		self.enemyEquipment = text.TextP('Enemy equipment: ' +str(assi.enemyEquipment))
		self.payment = text.TextP('Payment: ' +str(assi.payment))
		self.fame = text.TextP('Fame: ' +str(assi.fame))
	
	def draw(self):
		super().draw()
		self.title.draw()
		self.principal.draw()
		self.sectors.draw()
		self.enemyForce.draw()
		self.enemyLevel.draw()
		self.enemyEquipment.draw()
		self.payment.draw()
		self.fame.draw()
		
	def setPositions(self):
		x = self.rect.x +5
		y = self.rect.y +8
		self.title.setPosition(x, y)
		self.principal.setPosition(x, y +20)
		self.sectors.setPosition(x, y +40)
		self.enemyForce.setPosition(x, y +60)
		self.enemyLevel.setPosition(x, y +80)
		self.enemyEquipment.setPosition(x, y +100)
		self.payment.setPosition(x, y +120)
		self.fame.setPosition(x, y +140)

sectors = [
	'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4', 'Sector 5'
]

class State:
	assignment = 0
	enemy = 1


class AssignmentSection(section.Section):
	state = State.assignment
	def __init__(self, rect):
		super().__init__(rect)
		self.setAssignmentState()
	
	def setAssignmentState(self):
		self.state = State.assignment
		del self.focuses[:]
		self.addFocus(section.HeaderFocus('Assignments'))
		self.setCurrentFocusIndex(0)
		sf = AssignmentFocus(assignments.assignments[0])
		self.addFocus(sf)
		sf.setPositions()
		sf = AssignmentFocus(assignments.assignments[1])
		self.addFocus(sf)
		sf.setPositions()
	
	def setEnemyState(self):
		self.state = State.enemy
		del self.focuses[:]
		self.addFocus(section.HeaderFocus('Enemy'))
		self.setCurrentFocusIndex(0)
		for s in sectors:
			sf = SectorFocus(s)
			self.addFocus(sf)
			sf.setPositions()
	
	def space(self):
		"""Overwrite base behaviour"""
		if self.state == State.enemy:
			super().space()
		else:
			if self.currentFocusIndex in self.selection:
				self.selection.remove(self.currentFocusIndex)
			else:
				self.selection = set()
				self.selection.add(self.currentFocusIndex)
	
	
	def getFocusInfo(self):
		if self.state == State.assignment:
			if (self.currentFocusIndex == 0):
				heading = "Assignments"
				lines = [
					'Choose an assignment to begin',
					'battle!',
				]
			else:
				heading = self.currentFocus.title.title
				lines = [
					self.currentFocus.assignment.principal +' asks you',
					'to settle this issue.',
					'',
					'Battlefield size: ' +str(self.currentFocus.assignment.sectors),
					'Estimated enemy numbers: ' +str(self.currentFocus.assignment.enemyForce),
					'Estimated enemy level: ' +str(self.currentFocus.assignment.enemyLevel),
					'Estimated enemy equipment: ' +str(self.currentFocus.assignment.enemyEquipment),
					'',
					'Payment: ' +str(self.currentFocus.assignment.payment),
					'Fame   : ' +str(self.currentFocus.assignment.fame),
				]
		elif self.state == State.enemy:
			if (self.currentFocusIndex == 0):
				heading = "Enemy"
				lines = [
					'Enemy soldiers: x'
				]
			else:
				heading = self.currentFocus.title
				lines = [
					'Enemy sector soldiers: x'
				]
		return focus.FocusInfo(heading, lines)
		