import section
import item
import text
import assignments


class SectorItem(item.Item):
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


class AssignmentItem(item.Item):
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
		self.actions = [
			'Select this assignment',
		]
		
	
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
	
	def getInfo(self, activeActionId):
		heading = self.assignment.title
		lines = [
			self.assignment.principal + ' asks you',
			'to settle this issue.',
			'',
			'Battlefield size: ' + str(self.assignment.sectors),
			'Estimated enemy numbers: ' + str(self.assignment.enemyForce),
			'Estimated enemy level: ' + str(self.assignment.enemyLevel),
			'Estimated enemy equipment: ' + str(self.assignment.enemyEquipment),
			'',
			'Payment: ' + str(self.assignment.payment),
			'Fame   : ' + str(self.assignment.fame),
			]
		fi = item.ItemInfo(
			heading,
			lines,
			self.actions[activeActionId] + ':',
			)
		fi.setPositions()
		return fi
	
	
sectors = [
	'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4', 'Sector 5'
]

class State:
	assignment = 0
	enemy = 1

class AssignmentHeaderItem(item.HeaderItem):
	def __init__(self):
		super().__init__('Assignments')
		self.actions = [
			'Select assignment',
		]
	
	def getInfo(self, activeActionId):
		heading = 'Assignment'
		lines = [
			'Select Assignment and',
			'hit [Return] to start battle'
			]
		fi = item.ItemInfo(
			heading,
			lines,
			self.actions[activeActionId] + ':',
			)
		fi.setPositions()
		return fi


class AssignmentSection(section.Section):
	state = State.assignment
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.setAssignmentState()
	
	def setAssignmentState(self):
		self.state = State.assignment
		del self.items[:]
		self.addItem(AssignmentHeaderItem())
		self._setItemFocusIndex(0)
		sf = AssignmentItem(assignments.assignments[0])
		self.addItem(sf)
		sf = AssignmentItem(assignments.assignments[1])
		self.addItem(sf)
	
	def setEnemyState(self):
		self.state = State.enemy
		del self.items[:]
		self.addItem(item.HeaderItem('Enemy'))
		self._setItemFocusIndex(0)
		for s in sectors:
			sf = SectorItem(s)
			self.addItem(sf)
	
	def space(self):
		"""Overwrite base behaviour"""
		if self.state == State.enemy:
			super().space()
		else:
			if self.itemFocusIndex in self.selection:
				self.selection.remove(self.itemFocusIndex)
			else:
				self.selection = set()
				self.selection.add(self.itemFocusIndex)
	
	
	def getFocusInfo(self):
		if self.state == State.assignment:
			if (self.itemFocusIndex == 0):
				heading = "Assignments"
				lines = [
					'Choose an assignment to begin',
					'battle!',
				]
			else:
				heading = self.itemFocus.title.title
				lines = [
					self.itemFocus.assignment.principal + ' asks you',
					'to settle this issue.',
					'',
					'Battlefield size: ' + str(self.itemFocus.assignment.sectors),
					'Estimated enemy numbers: ' + str(self.itemFocus.assignment.enemyForce),
					'Estimated enemy level: ' + str(self.itemFocus.assignment.enemyLevel),
					'Estimated enemy equipment: ' + str(self.itemFocus.assignment.enemyEquipment),
					'',
					'Payment: ' + str(self.itemFocus.assignment.payment),
					'Fame   : ' + str(self.itemFocus.assignment.fame),
				]
		elif self.state == State.enemy:
			if (self.itemFocusIndex == 0):
				heading = "Enemy"
				lines = [
					'Enemy soldiers: x'
				]
			else:
				heading = self.itemFocus.title
				lines = [
					'Enemy sector soldiers: x'
				]
		return item.ItemInfo(heading, lines)
		