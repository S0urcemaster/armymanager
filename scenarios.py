import assignments as assigns
import lib

class Scenario:
	def __init__(self):
		self.assignment = None
		self.assignments = []
		self.army = None
		self.mercs = []
		self.recruits = []


class PfullingScenario(Scenario):
	def __init__(self):
		super().__init__()
		self.assignment = assigns.Assignment(
			title = 'Bandits around Pfulling',
			principal = 'Mayor of Pfulling',
			sectors = 1,
			payment = 1.5,
			fame= 10,
			enemyForce = 10,
			enemyLevel = 0,
			enemyEquipment = 0,
			fogFactor = 0,
			army = lib.randomArmy(1, 10),
		)
		self.army = lib.randomArmy(1, 10)


class OfenhaufnScenario(Scenario):
	def __init__(self):
		super().__init__()
		self.assignment = assigns.Assignment(
			title = 'Attack Ofenhaufn',
			principal = 'Duke of Graveneck',
			sectors = 1,
			payment = 5,
			fame= 10,
			enemyForce = 100,
			enemyLevel = 0,
			enemyEquipment = 0,
			fogFactor = 0,
			army = lib.randomArmy(1, 100),
		)
		self.army = lib.randomArmy(1, 100)