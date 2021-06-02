import army
import merc as merci

class BfSector:
	def __init__(self):
		self.troops: army.Sector
		self.busyTroops = army.Sector
		self.enemy: army.Sector
		self.busyEnemy = army.Sector
		self.conflicted = []
	
	def conflict(self):
		busyT = self.troops.pikemen[0:33]
		busyE = self.enemy.pikemen[0:33]
		self.conflicted = list(zip(busyT, busyE))
		if len(self.conflicted) == 0:
			return False
		self.busyTroops.pikemen = self.troops.pikemen[:len(self.conflicted)]
		self.troops.pikemen = self.troops.pikemen[len(self.conflicted):]
		self.busyEnemy.pikemen = self.enemy.pikemen[:len(self.conflicted)]
		self.enemy.pikemen = self.enemy.pikemen[len(self.conflicted):]
		return self.conflicted
	
	def returnTroopFromConflict(self, merc):
		if merc.xp.typ == merci.UnitType.pikeman:
			self.troops.pikemen.append(merc)
		if merc.xp.typ == merci.UnitType.cavalry:
			self.troops.cavalryMen.append(merc)
		if merc.xp.typ == merci.UnitType.musketeer:
			self.troops.musketeer.append(merc)
	
	def returnEnemyFromConflict(self, merc):
		if merc.xp.typ == merci.UnitType.pikeman:
			self.troops.pikemen.append(merc)
		if merc.xp.typ == merci.UnitType.cavalry:
			self.troops.cavalryMen.append(merc)
		if merc.xp.typ == merci.UnitType.musketeer:
			self.troops.musketeer.append(merc)
	
	def kia(self, pair):
		if pair[0].wounds <4:
			self.returnTroopFromConflict(pair[0])
		if pair[1].wounds <4:
			self.returnEnemyFromConflict(pair[1])
		self.conflicted.remove(pair)


class Battlefield:
	troops: army.Army
	enemy: army.Army
	
	sectors = []
	
	def __init__(self, troops, enemy):
		self.troops = troops
		self.enemy = enemy
		for sx, s in enumerate(troops.sectors):
			self.sectors[sx] = BfSector()
			self.sectors[sx].troops = s
		for sx, s in enumerate(enemy.sectors):
			self.sectors[sx].troops = s
	
		
	