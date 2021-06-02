import merc

class Sector:
	"""
	A sector has room for 100 soldiers to fight simultaneously
	and can hold up to 1000 at all
	"""
	def __init__(self, title, pikemen = [], cavalryMen = [], musketeers = []):
		self.title = title
		self.pikemen = pikemen
		self.cavalryMen = cavalryMen
		self.musketeers = musketeers
		self.total = len(pikemen) +len(cavalryMen) +len(musketeers)
	
	def pickHealthiestPikeman(self):
		for p in self.pikemen:
			if p.wound == merc.Wounds.none: return p
		for p in self.pikemen:
			if p.wound == merc.Wounds.slightyInjured1: return p
		for p in self.pikemen:
			if p.wound == merc.Wounds.slightyInjured2: return p
		for p in self.pikemen:
			if p.wound == merc.Wounds.seriouslyInjured: return p
	

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