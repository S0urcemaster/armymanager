import pygame
import section
import item
import text
import merc
import color
import events

trainPikeman1 = 'Train Pikeman (1)'
trainCavalry1 = 'Train Cavalry (1)'
trainMusketeer1 = 'Train Musketeer (1)'
trainPikeman2 = 'Train Pikeman (2)'
trainCavalry2 = 'Train Cavalry (2)'
trainMusketeer2 = 'Train Musketeer (2)'

class MercItem(item.Item):
	def __init__(self, soldier: merc.Merc):
		super().__init__(85)
		self.soldier = soldier
		self.actions = []
		if soldier.xp.typ == merc.UnitType.recruit:
			self.actions.append(trainPikeman1)
			self.actions.append(trainCavalry1)
			self.actions.append(trainMusketeer1)
		elif soldier.xp.getLevel() == 1:
			if soldier.xp.typ == merc.UnitType.pikeman:
				self.actions.append(trainPikeman2)
			elif soldier.xp.typ == merc.UnitType.cavalry:
				self.actions.append(trainCavalry2)
			elif soldier.xp.typ == merc.UnitType.musketeer:
				self.actions.append(trainMusketeer2)
		# elif soldier.xp
		self.name = text.TextH(f"{soldier.firstname} {soldier.lastname} - {soldier.getAge(events.Event.current)}")
		self.pay = text.TextH(str(soldier.pay), col = color.silver)
		self.perks = []
		for p in soldier.perks:
			if sum(p.factors) >0: col = color.greenDark
			elif sum(p.factors) <0: col = color.redDark
			else: col = color.black
			self.perks.append(text.TextP(p.name, col = col))
	
	def draw(self):
		super().draw()
		self.name.draw()
		self.pay.draw()
		for p in self.perks:
			p.draw()
		pygame.draw.line(self.screen, color.red, (self.rect.x +7, self.rect.y +35),
		                 (self.rect.x + self.soldier.strength / 2 + 7, self.rect.y + 35), 8)
		pygame.draw.line(self.screen, color.green, (self.rect.x +7, self.rect.y +45),
		                 (self.rect.x + self.soldier.dexterity / 2 + 7, self.rect.y + 45), 8)
		pygame.draw.line(self.screen, color.blue, (self.rect.x +7, self.rect.y +55),
		                 (self.rect.x + self.soldier.intelligence / 2 + 7, self.rect.y + 55), 8)
		pygame.draw.line(self.screen, color.yellow, (self.rect.x +7, self.rect.y +65),
		                 (self.rect.x + self.soldier.charisma / 2 + 7, self.rect.y + 65), 8)
		pygame.draw.line(self.screen, color.purple, (self.rect.x +7, self.rect.y +75),
		                 (self.rect.x + self.soldier.confidence / 2 + 7, self.rect.y + 75), 8)
	
	def setPositions(self):
		self.name.setPosition(self.rect.x +7, self.rect.y +6)
		self.pay.setPosition(self.rect.x +self.rect.w -30, self.rect.y +6)
		for i, p in enumerate(self.perks):
			p.setPosition(self.rect.x +self.rect.w -70, self.rect.y +25 +i *20)
	
	def getInfo(self, activeActionId):
		heading = self.soldier.firstname + ' ' + self.soldier.lastname
		lines = [
			'Age: ' +str(self.soldier.getAge(events.Event.current)),
			'Training: ' +self.soldier.xp.typ,
			'Experience: ' +str(self.soldier.xp.xp),
			'Pay: ' +str(self.soldier.pay),
			'Pockets: ' +str(self.soldier.asset),
			'Strength: ' +str(self.soldier.strength),
			'Dexterity: ' +str(self.soldier.dexterity),
			'Intelligence: ' +str(self.soldier.intelligence),
			'Charisma: ' +str(self.soldier.charisma),
			'Confidence: ' +str(self.soldier.confidence),
			]
		for p in self.soldier.perks:
			lines.append(p.name)
		fi = item.ItemInfo(
			heading,
			lines,
			self.actions[activeActionId] +':',
			)
		fi.setPositions()
		return fi


class CampHeaderItem(item.HeaderItem):
	def __init__(self):
		super().__init__('Camp')
		self.actions = [
			'Equip all visible next level'
		]
	
	def getInfo(self, activeActionId):
		heading = 'Camp'
		lines = [
			'Total mercenaries: ' +str(10),
			]
		fi = item.ItemInfo(
			heading,
			lines,
			self.actions[activeActionId] +':',
			)
		fi.setPositions()
		return fi


class CampSection(section.Section):
	
	soldiers = []
	
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addFocus(CampHeaderItem())
		self._setItemFocusIndex(0)
	
	def initialMercs(self, recruits):
		self.soldiers.extend(recruits)
		del self.items[1:]
		for r in recruits:
			f = MercItem(r)
			self.addFocus(f)
			
	def update(self):
		del self.items[1:]
		for s in self.soldiers:
			f = MercItem(s)
			self.addFocus(f)
		
			
	def action(self, command):
		if command == trainPikeman1:
			for s in self.selectedItemsIndices:
				s.soldier.xp.train(merc.UnitType.pikeman)
		if command == trainCavalry1:
			for s in self.selectedItemsIndices:
				s.soldier.xp.train(merc.UnitType.cavalry)
		if command == trainMusketeer1:
			for s in self.selectedItemsIndices:
				s.soldier.xp.train(merc.UnitType.musketeer)
		if command == trainPikeman2:
			for s in self.selectedItemsIndices:
				s.soldier.xp.levelUp()
		if command == trainCavalry2:
			for s in self.selectedItemsIndices:
				s.soldier.xp.levelUp()
		if command == trainMusketeer2:
			for s in self.selectedItemsIndices:
				s.soldier.xp.levelUp()
		self.update()
			
			