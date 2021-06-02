import section
import item
import text
import assignments
import sections.troops as troops
import army


class SectorItem(troops.SectorItem):
	def __init__(self, sector: army.Sector):
		super().__init__(sector)
		actions = [
			'Action 1',
			'Action 2',
			'Action 3',
		]
		self.info = item.ItemInfo(
			self.sector.title,
			[
				'Enemy force estimations:',
				'Total: 10',
				'Pikeman: 10',
				'Cavalry: 0',
				'Musketeers: 0',
				'Training level: 0',
				'Equipment level: 0',
				],
			actions,
		)
	
	def draw(self):
		super().draw()
		# self.name.draw()
	
	def setPositions(self):
		rect = self.title.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.title.setPosition(self.rect.x +rect.x, self.rect.y +5)


selectThisAssignment = 'Select this assignment'
attack = 'Attack!'

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
		actions = [
			selectThisAssignment,
		]
		self.info = item.ItemInfo(
			self.assignment.title,
			[
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
				],
			actions,
		)
		
	
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
	
	
# sectors = [
# 	'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4', 'Sector 5'
# ]

class State:
	assignment = 0
	enemy = 1

class AssignmentHeaderItem(item.HeaderItem):
	def __init__(self):
		super().__init__('Assignments')
		actions = [
			'Select assignment',
		]
		self.info = item.ItemInfo('Assignment',
			[
				'Select Assignment and',
				'hit [Return] to start battle'
			], actions,
		)

class SectorHeaderItem(item.HeaderItem):
	def __init__(self):
		super().__init__('Enemy')
		actions = [
			'Spy out',
			attack,
		]
		self.info = item.ItemInfo('Assignment',
			[
				'Enemy force estimations:',
				'Total: 9999',
				'Pikeman: 9999',
				'Cavalry: 999',
				'Musketeers: 9999',
				'Training level: 1',
				'Equipment level: 1',
			], actions,
		)


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
	
	# def setEnemyState(self):
	# 	self.state = State.enemy
	# 	del self.items[:]
	# 	self.addItem(item.HeaderItem('Enemy'))
	# 	self._setItemFocusIndex(0)
	# 	for s in sectors:
	# 		sf = SectorItem(s)
	# 		self.addItem(sf)
	
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
	
	
	def assignmentChanged(self, assignment):
		del self.items[:] # switch assignment view to enemy view:
		self.addItem(SectorHeaderItem())
		for i in range(assignment.sectors):
			self.addItem(SectorItem(assignment.army.sectors[i]))
	
	def setAssignment(self, assignment):
		self.assignmentChanged(assignment)
		
	def act(self, action):
		info = self.items[self.itemFocusIndex].info
		if info.actions[action] == selectThisAssignment:
			self.game.selectThisAssignment(self.itemFocus.assignment) # adjust and activate troups section
		if info.actions[action] == attack:
			self.game.battle()