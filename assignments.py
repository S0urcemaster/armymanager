
class Assignment:
	def __init__(self, title, principal, sectors, payment, fame,
	             enemyForce, enemyLevel, enemyEquipment):
		self.title = title
		self.principal = principal
		self.sectors = sectors
		self.payment = payment
		self.fame = fame
		self.enemyForce = enemyForce
		self.enemyLevel = enemyLevel
		self.enemyEquipment = enemyEquipment

# Ofenhaufn
# Ening
# Deting
# Graveneck
# Zwiefaltn
# Rietling
# Tübingen
# Lustnau
# Tusling

assignments = [
	Assignment(
		title = 'Bandits around Pfulling',
		principal = 'Mayor of Pfulling',
		sectors = 1,
		payment = 1.5,
		fame= 10,
		enemyForce = 10,
		enemyLevel = 0,
		enemyEquipment = 0,
	),
	Assignment(
		title = 'Bandits around Deting',
		principal = 'Mayor of Deting',
		sectors = 1,
		payment = 1.5,
		fame= 15,
		enemyForce = 15,
		enemyLevel = 0,
		enemyEquipment = 0,
	),
	# Assignment(
	# 	title = '',
	# 	principal = '',
	# 	sectors = 1,
	# 	estimatedEnemyForce = 10,
	# 	payment = 1.5,
	# 	reputation = 10,
	# ),
]