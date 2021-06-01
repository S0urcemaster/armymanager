import merc

class Sector:
	
	def __init__(self, title):
		self.title = title
		self.pikemen = []
		self.cavalryMen = []
		self.musketeers = []
	

class Army:
	
	sectors = []
	
	def __init__(self, numSectors = 0):
		for i in range(0, numSectors):
			self.sectors.append(Sector('Sector ' +str(i +1)))
	
	def getNoofPikeman(self):
		sum = 0
		for s in self.sectors:
			sum += len(s.pikemen)
		return sum