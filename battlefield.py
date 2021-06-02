import army
import merc as merci

class BfSector:
	def __init__(self, troops: army.Sector, enemy: army.Sector):
		self.troops = army.Sector(troops.pikemen[:], troops.cavalryMen[:], troops.musketeers[:])
		self.busyTroops = army.Sector(troops.title)
		self.enemy = army.Sector(enemy.pikemen[:], enemy.cavalryMen[:], enemy.musketeers[:])
		self.busyEnemy = army.Sector(enemy.title)
		self.conflictedPikemen = []
	
	def conflictPikemen(self):
		busyT = self.troops.pikemen[0:33]
		busyE = self.enemy.pikemen[0:33]
		self.conflictedPikemen = list(zip(busyT, busyE))
		if len(self.conflictedPikemen) == 0:
			return False
		self.busyTroops.pikemen = self.troops.pikemen[:len(self.conflictedPikemen)]
		self.troops.pikemen = self.troops.pikemen[len(self.conflictedPikemen):]
		self.busyEnemy.pikemen = self.enemy.pikemen[:len(self.conflictedPikemen)]
		self.enemy.pikemen = self.enemy.pikemen[len(self.conflictedPikemen):]
		return self.conflictedPikemen
	
	def returnTroopFromConflict(self, merc):
		if merc.xp.typ == merci.UnitType.pikeman:
			self.troops.pikemen.append(merc)
		if merc.xp.typ == merci.UnitType.cavalry:
			self.troops.cavalryMen.append(merc)
		if merc.xp.typ == merci.UnitType.musketeer:
			self.troops.musketeers.append(merc)
	
	def returnEnemyFromConflict(self, merc):
		if merc.xp.typ == merci.UnitType.pikeman:
			self.troops.pikemen.append(merc)
		if merc.xp.typ == merci.UnitType.cavalry:
			self.troops.cavalryMen.append(merc)
		if merc.xp.typ == merci.UnitType.musketeer:
			self.troops.musketeers.append(merc)
	
	def kia(self, pair):
		if pair[0].wounds <4:
			self.returnTroopFromConflict(pair[0])
		if pair[1].wounds <4:
			self.returnEnemyFromConflict(pair[1])
		self.conflictedPikemen.remove(pair)
		if len(self.conflictedPikemen):
			self.conflictPikemen()


class Battlefield:
	troops: army.Army
	enemy: army.Army
	
	sectors = []
	
	def __init__(self, troops, enemy):
		self.troops = troops
		self.enemy = enemy
		for sx, s in enumerate(troops.sectors):
			self.sectors.append(BfSector(s, enemy.sectors[sx]))
	
	def conflictGoing(self):
		for s in self.sectors:
			if len(s.busyTroops.pikemen) >0: return True
			if len(s.busyEnemy.pikemen) >0: return True
		
	