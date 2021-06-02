import merc

class Sector:
	
	def __init__(self, title, pikemen = [], cavalryMen = [], musketeers = []):
		self.title = title
		self.pikemen = pikemen
		self.cavalryMen = cavalryMen
		self.musketeers = musketeers
		self.total = len(pikemen) +len(cavalryMen) +len(musketeers)
	

class Army:
	
	def __init__(self, numSectors = 0):
		self.sectors = []
		for i in range(0, numSectors):
			self.sectors.append(Sector('Sector ' +str(i +1)))
	
	def getNoofPikeman(self):
		sum = 0
		for s in self.sectors:
			sum += len(s.pikemen)
		return sum
	
	def getTotalMercs(self):
		t = 0
		for s in self.sectors:
			t += s.total
		return t