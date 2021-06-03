import army
import merc as merci

class BfSector:
	def __init__(self, troops: army.Sector, enemy: army.Sector):
		self.troops = army.Sector(troops.title, troops.pikemen[:], troops.cavalryMen[:], troops.musketeers[:])
		self.busyTroops = army.Sector(troops.title)
		self.enemy = army.Sector(troops.title, enemy.pikemen[:], enemy.cavalryMen[:], enemy.musketeers[:])
		self.busyEnemy = army.Sector(enemy.title)
		self.conflictedPikemen = []
		self.conflictedCavalryMen = []
		self.conflictedMusketeers = []
	
	def conflicPikemen(self):
		busyT = self.troops.pikemen[0:34] # initial amount
		busyE = self.enemy.pikemen[0:34] # dead opponents will be replaced on kill
		self.conflictedPikemen = list(zip(busyT, busyE)) # pair up
		if len(self.conflictedPikemen) == 0:
			return False
		self.busyTroops.pikemen = self.troops.pikemen[:len(self.conflictedPikemen)]
		self.troops.pikemen = self.troops.pikemen[len(self.conflictedPikemen):]
		self.busyEnemy.pikemen = self.enemy.pikemen[:len(self.conflictedPikemen)]
		self.enemy.pikemen = self.enemy.pikemen[len(self.conflictedPikemen):]
		return self.conflictedPikemen
	
	def conflictCavalryMen(self):
		busyT = self.troops.cavalryMen[0:34]
		busyE = self.enemy.cavalryMen[0:34]
		self.conflictedCavalryMen = list(zip(busyT, busyE))
		if len(self.conflictedCavalryMen) == 0:
			return False
		self.busyTroops.cavalryMen = self.troops.cavalryMen[:len(self.conflictedCavalryMen)]
		self.troops.cavalryMen = self.troops.cavalryMen[len(self.conflictedCavalryMen):]
		self.busyEnemy.cavalryMen = self.enemy.cavalryMen[:len(self.conflictedCavalryMen)]
		self.enemy.cavalryMen = self.enemy.cavalryMen[len(self.conflictedCavalryMen):]
		return self.conflictedCavalryMen
	
	def conflictMusketeers(self):
		busyT = self.troops.musketeers[0:34]
		busyE = self.enemy.musketeers[0:34]
		self.conflictedMusketeers = list(zip(busyT, busyE))
		if len(self.conflictedMusketeers) == 0:
			return False
		self.busyTroops.musketeers = self.troops.musketeers[:len(self.conflictedMusketeers)]
		self.troops.musketeers = self.troops.musketeers[len(self.conflictedMusketeers):]
		self.busyEnemy.musketeers = self.enemy.musketeers[:len(self.conflictedMusketeers)]
		self.enemy.musketeers = self.enemy.musketeers[len(self.conflictedMusketeers):]
		return self.conflictedMusketeers
	
	def returnTroopFromConflict(self, merc):
		if merc.xp.typ == merci.UnitType.pikeman:
			self.troops.pikemen.append(merc)
			self.busyTroops.pikemen.remove(merc)
		elif merc.xp.typ == merci.UnitType.cavalry:
			self.troops.cavalryMen.append(merc)
			self.busyTroops.cavalryMen.remove(merc)
		elif merc.xp.typ == merci.UnitType.musketeer:
			self.troops.musketeers.append(merc)
			self.busyTroops.musketeers.remove(merc)
	
	def returnEnemyFromConflict(self, merc):
		if merc.xp.typ == merci.UnitType.pikeman:
			self.enemy.pikemen.append(merc)
			self.busyEnemy.pikemen.remove(merc)
		elif merc.xp.typ == merci.UnitType.cavalry:
			self.enemy.cavalryMen.append(merc)
			self.busyEnemy.cavalryMen.remove(merc)
		elif merc.xp.typ == merci.UnitType.musketeer:
			self.enemy.musketeers.append(merc)
			self.busyEnemy.musketeers.remove(merc)
	
	def returnTroopFromBusy(self, merc):
		if merc.xp.typ == merci.UnitType.pikeman:
			self.busyTroops.pikemen.remove(merc)
			self.troops.pikemen.append(merc)
		elif merc.xp.typ == merci.UnitType.cavalry:
			self.busyTroops.cavalryMen.remove(merc)
			self.troops.cavalryMen.append(merc)
		elif merc.xp.typ == merci.UnitType.musketeer:
			self.busyTroops.musketeers.remove(merc)
			self.troops.musketeers.append(merc)
	
	def returnEnemyFromBusy(self, merc):
		if merc.xp.typ == merci.UnitType.pikeman:
			self.busyEnemy.pikemen.remove(merc)
			self.enemy.pikemen.append(merc)
		elif merc.xp.typ == merci.UnitType.cavalry:
			self.busyEnemy.cavalryMen.remove(merc)
			self.enemy.cavalryMen.append(merc)
		elif merc.xp.typ == merci.UnitType.musketeer:
			self.busyEnemy.musketeers.remove(merc)
			self.enemy.musketeers.append(merc)
	
	def removeEnemyFromBusy(self, merc):
		"""got killed"""
		if merc.xp.typ == merci.UnitType.pikeman:
			self.busyEnemy.pikemen.remove(merc)
		elif merc.xp.typ == merci.UnitType.cavalry:
			self.busyEnemy.cavalryMen.remove(merc)
		elif merc.xp.typ == merci.UnitType.musketeer:
			self.busyEnemy.musketeers.remove(merc)
	
	def removeTroopFromBusy(self, merc):
		"""got killed"""
		if merc.xp.typ == merci.UnitType.pikeman:
			self.busyTroops.pikemen.remove(merc)
		elif merc.xp.typ == merci.UnitType.cavalry:
			self.busyTroops.cavalryMen.remove(merc)
		elif merc.xp.typ == merci.UnitType.musketeer:
			self.busyTroops.musketeers.remove(merc)
	
	def removePairFromConflict(self, pair):
		# try:
			if pair[0].xp.typ == merci.UnitType.pikeman and pair[1].xp.typ == merci.UnitType.pikeman:
				self.conflictedPikemen.remove(pair)
			elif pair[0].xp.typ == merci.UnitType.cavalry and pair[1].xp.typ == merci.UnitType.cavalry:
				self.conflictedCavalryMen.remove(pair)
			elif pair[0].xp.typ == merci.UnitType.musketeer and pair[1].xp.typ == merci.UnitType.musketeer:
				self.conflictedMusketeers.remove(pair)
		# except:
		# 	pass
	
	def replaceTroop(self, pair):
		"""find new match"""
		self.removeTroopFromBusy(pair[0]) # dead
		enemy = pair[1]
		if enemy.xp.typ == merci.UnitType.pikeman:
			if len(self.troops.pikemen) >0: # favorite match
				p = self.troops.pikemen.pop(0)
				self.busyTroops.pikemen.append(p)
				self.removePairFromConflict(pair)
				newPair = (p, pair[1])
				self.conflictedPikemen.append(newPair)
				print(f'Troop replaced [{newPair[0].firstname} {newPair[0].lastname} {newPair[0].wounds} {newPair[0].xp.typ}]')
				return newPair
			else:
				# self.returnEnemyFromBusy(enemy) # survived
				self.removePairFromConflict(pair)
		elif enemy.xp.typ == merci.UnitType.cavalry:
			if len(self.troops.cavalryMen) >0: # favorite match
				p = self.troops.cavalryMen.pop(0)
				self.busyTroops.cavalryMen.append(p)
				self.removePairFromConflict(pair)
				newPair = (p, pair[1])
				self.conflictedCavalryMen.append(newPair)
				print(f'Troop replaced [{newPair[0].firstname} {newPair[0].lastname} {newPair[0].wounds} {newPair[0].xp.typ}]')
				return newPair
			else:
				# self.returnEnemyFromBusy(enemy) # survived
				self.removePairFromConflict(pair)
		elif enemy.xp.typ == merci.UnitType.musketeer:
			if len(self.troops.musketeers) >0: # favorite match
				p = self.troops.musketeers.pop(0)
				self.busyTroops.musketeers.append(p)
				self.removePairFromConflict(pair)
				newPair = (p, pair[1])
				self.conflictedMusketeers.append(newPair)
				print(f'Troop replaced [{newPair[0].firstname} {newPair[0].lastname} {newPair[0].wounds} {newPair[0].xp.typ}]')
				return newPair
			else:
				# self.returnEnemyFromBusy(enemy) # survived
				self.removePairFromConflict(pair)
		return False
	
	def replaceEnemy(self, pair):
		"""find new match"""
		self.removeEnemyFromBusy(pair[1]) # dead
		troop = pair[0]
		if troop.xp.typ == merci.UnitType.pikeman:
			if len(self.enemy.pikemen) >0: # favorite match
				p = self.enemy.pikemen.pop(0)
				self.busyEnemy.pikemen.append(p)
				self.removePairFromConflict(pair)
				newPair = (troop, p)
				self.conflictedPikemen.append(newPair)
				print(f'Enemy replaced [{newPair[1].firstname} {newPair[1].lastname} {newPair[1].wounds} {newPair[1].xp.typ}]')
				return newPair
			# elif len(self.enemy.cavalryMen) >0: # advantage
			# 	pass
			# elif len(self.enemy.musketeers) >0: # disadvantage
			# 	pass
			else:
				# self.returnTroopFromBusy(troop) # survived
				self.removePairFromConflict(pair)
		elif troop.xp.typ == merci.UnitType.cavalry:
			if len(self.enemy.cavalryMen) >0:
				p = self.enemy.cavalryMen.pop(0)
				self.busyEnemy.cavalryMen.append(p)
				self.removePairFromConflict(pair)
				newPair = (troop, p)
				self.conflictedCavalryMen.append(newPair)
				print(f'Enemy replaced [{newPair[1].firstname} {newPair[1].lastname} {newPair[1].wounds} {newPair[1].xp.typ}]')
				return newPair
			else:
				# self.returnTroopFromBusy(troop) # survived
				self.removePairFromConflict(pair)
		elif troop.xp.typ == merci.UnitType.musketeer:
			if len(self.enemy.musketeers) >0:
				p = self.enemy.musketeers.pop(0)
				self.busyEnemy.musketeers.append(p)
				self.removePairFromConflict(pair)
				newPair = (troop, p)
				self.conflictedMusketeers.append(newPair)
				print(f'Enemy replaced [{newPair[1].firstname} {newPair[1].lastname} {newPair[1].wounds} {newPair[1].xp.typ}]')
				return newPair
			else:
				# self.returnTroopFromBusy(troop) # survived
				self.removePairFromConflict(pair)
		return False
	
	def kia(self, pair):
		"""returns updated pair if there are reinforcements, false if not"""
		if pair[0].wounds <4: # troop survived
			print(f'Enemy killed [{pair[1].firstname} {pair[1].lastname} {pair[1].wounds} {pair[1].xp.typ}]')
			# replacement?
			newPair = self.replaceEnemy(pair)
			if newPair:
				return newPair
			self.returnTroopFromConflict(pair[0])
			return False
		if pair[1].wounds <4: # enemy survived
			print(f'Troop killed [{pair[0].firstname} {pair[0].lastname} {pair[0].wounds} {pair[1].xp.typ}]')
			# replacement?
			newPair = self.replaceTroop(pair)
			if newPair:
				return newPair
			self.returnEnemyFromConflict(pair[1])
			return False


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
		
	def getArmies(self):
		arm = army.Army(len(self.sectors))
		enemy = army.Army(len(self.sectors))
		for sx, s in enumerate(self.sectors):
			arm.sectors[sx].pikemen = s.troops.pikemen +s.busyTroops.pikemen
			arm.sectors[sx].cavalryMen = s.troops.cavalryMen +s.busyTroops.cavalryMen
			arm.sectors[sx].musketeers = s.troops.musketeers +s.busyTroops.musketeers
			enemy.sectors[sx].pikemen = s.enemy.pikemen +s.busyEnemy.pikemen
			enemy.sectors[sx].cavalryMen = s.enemy.cavalryMen +s.busyEnemy.cavalryMen
			enemy.sectors[sx].musketeers = s.enemy.musketeers +s.busyEnemy.musketeers
		return (arm, enemy)
	
	# def sideWon(self):
	# 	if