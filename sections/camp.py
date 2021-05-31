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
	
	pikemanImg = pygame.image.load('res/pikeman.png')
	cavalryImg = pygame.image.load('res/cavalry.png')
	musketeerImg = pygame.image.load('res/musketeer.png')
	
	def __init__(self, soldier: merc.Merc):
		super().__init__(85)
		self.soldier = soldier
		self.rect = None
		self.name = text.TextH(f"{soldier.firstname} {soldier.lastname} - {soldier.getAge(events.Event.current)}")
		self.pay = text.TextH(str(soldier.pay), col = color.silver)
		self.perks = []
		for p in soldier.perks:
			if sum(p.factors) >0: col = color.greenDark
			elif sum(p.factors) <0: col = color.redDark
			else: col = color.black
			self.perks.append(text.TextP(p.name, col = col))
		
		actions = []
		if soldier.xp.typ == merc.UnitType.recruit:
			actions.append(trainPikeman1)
			actions.append(trainCavalry1)
			actions.append(trainMusketeer1)
		elif soldier.xp.getLevel() == 1:
			if soldier.xp.typ == merc.UnitType.pikeman:
				actions.append(trainPikeman2)
			elif soldier.xp.typ == merc.UnitType.cavalry:
				actions.append(trainCavalry2)
			elif soldier.xp.typ == merc.UnitType.musketeer:
				actions.append(trainMusketeer2)
		
		self.info = item.ItemInfo(
			self.soldier.firstname + ' ' + self.soldier.lastname,
			[
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
				], actions
		)
	
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
		
		r = pygame.Rect(self.rect.x +200, self.rect.y +30, 50, 50)
		if self.soldier.xp.typ == merc.UnitType.pikeman:
			self.screen.blit(self.pikemanImg, r)
		if self.soldier.xp.typ == merc.UnitType.cavalry:
			self.screen.blit(self.cavalryImg, r)
		if self.soldier.xp.typ == merc.UnitType.musketeer:
			self.screen.blit(self.musketeerImg, r)
	
	def setPositions(self):
		self.name.setPosition(self.rect.x +7, self.rect.y +6)
		self.pay.setPosition(self.rect.x +self.rect.w -30, self.rect.y +6)
		for i, p in enumerate(self.perks):
			p.setPosition(self.rect.x +self.rect.w -70, self.rect.y +25 +i *20)
	
	def action(self, id):
		if self.info.actions[id] == trainPikeman1:
			self.soldier.xp.train(merc.UnitType.pikeman)
		if self.info.actions[id] == trainCavalry1:
			self.soldier.xp.train(merc.UnitType.cavalry)
		if self.info.actions[id] == trainMusketeer1:
			self.soldier.xp.train(merc.UnitType.musketeer)
		if self.info.actions[id] == trainPikeman2:
			self.soldier.xp.levelUp()
		if self.info.actions[id] == trainCavalry2:
			self.soldier.xp.levelUp()
		if self.info.actions[id] == trainMusketeer2:
			self.soldier.xp.levelUp()

class CampHeaderItem(item.HeaderItem):
	def __init__(self):
		super().__init__('Camp')
		actions = [
			'Equip all visible next level'
		]
		self.info = item.ItemInfo('Camp',['Total mercenaries: ' +str(10)], actions)


class CampSection(section.Section):
	
	listIndex = 0
	
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addItem(CampHeaderItem())
		self._setItemFocusIndex(0)
		self.stats = section.SectionStats(0, self.rect)
		self.listMarker = section.ScrollBar(self.rect)
	
	def draw(self):
		super().draw()
		self.listMarker.draw()
		self.stats.draw()
			
	def setMercs(self, mercs):
		# self.soldiers = mercs
		del self.items[1:]
		for r in mercs[self.listIndex *10:self.listIndex *10 +10]:
			f = MercItem(r)
			self.addItem(f)
		self.stats.update(len(mercs))
		self.listMarker.update(self.listIndex, len(mercs))
	
	
	def act(self, action):
		info = self.items[self.itemFocusIndex].info
		if info.actions[action] == trainPikeman1:
			self.game.doTrain(self.items[self.itemFocusIndex].soldier, merc.UnitType.pikeman)
		if info.actions[action] == trainCavalry1:
			self.game.doTrain(self.items[self.itemFocusIndex].soldier, merc.UnitType.cavalry)
		if info.actions[action] == trainMusketeer1:
			self.game.doTrain(self.items[self.itemFocusIndex].soldier, merc.UnitType.musketeer)
			
	