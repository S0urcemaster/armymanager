
class Sector:
	def __init__(self, title):
		self.title = title
	mercs = []

class Army:
	sectors = []
	def __init__(self, numSectors = 0):
		for i in range(0, numSectors):
			self.sectors.append(Sector('Sector ' +str(i +1)))