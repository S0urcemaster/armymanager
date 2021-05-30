import pygame.draw

import section
import item
import text
import color
import merc
import events

recruitSelected = 'Recruit selected'
dismissSelected = 'Dismiss selected'
nextRecruits = 'Next Recruits'
previousRecruits = 'Previous Recruits'

class RecruitItem(item.Item):
	def __init__(self, recruit: merc.Merc):
		super().__init__(85)
		self.recruit:merc.Merc = recruit
		self.actions = []
		self.actions.append(recruitSelected)
		self.actions.append(dismissSelected)
		self.actions.append(nextRecruits)
		self.actions.append(previousRecruits)
		self.name = text.TextH(f"{recruit.firstname} {recruit.lastname} - {recruit.getAge(events.Event.current)}")
		self.pay = text.TextH(str(recruit.pay), col = color.silver)
		self.perks = []
		for p in recruit.perks:
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
						 (self.rect.x +self.recruit.strength /2 +7, self.rect.y +35), 8)
		pygame.draw.line(self.screen, color.green, (self.rect.x +7, self.rect.y +45),
						 (self.rect.x +self.recruit.dexterity /2 +7, self.rect.y +45), 8)
		pygame.draw.line(self.screen, color.blue, (self.rect.x +7, self.rect.y +55),
						 (self.rect.x +self.recruit.intelligence /2 +7, self.rect.y +55), 8)
		pygame.draw.line(self.screen, color.yellow, (self.rect.x +7, self.rect.y +65),
						 (self.rect.x +self.recruit.charisma /2 +7, self.rect.y +65), 8)
		pygame.draw.line(self.screen, color.purple, (self.rect.x +7, self.rect.y +75),
						 (self.rect.x +self.recruit.confidence /2 +7, self.rect.y +75), 8)

	def setPositions(self):
		self.name.setPosition(self.rect.x +7, self.rect.y +6)
		self.pay.setPosition(self.rect.x +self.rect.w -30, self.rect.y +6)
		for i, p in enumerate(self.perks):
			p.setPosition(self.rect.x +self.rect.w -70, self.rect.y +25 +i *20)
	
	def getInfo(self, activeActionId):
		heading = self.recruit.firstname +' ' +self.recruit.lastname
		lines = [
			'Age: ' +str(self.recruit.getAge(events.Event.current)),
			'Training: ' +self.recruit.xp.typ,
			'Experience: ' +str(self.recruit.xp.xp),
			'Pay: ' +str(self.recruit.pay),
			'Pockets: ' +str(self.recruit.asset),
			'Strength: ' +str(self.recruit.strength),
			'Dexterity: ' +str(self.recruit.dexterity),
			'Intelligence: ' +str(self.recruit.intelligence),
			'Charisma: ' +str(self.recruit.charisma),
			'Confidence: ' +str(self.recruit.confidence),
			]
		for p in self.recruit.perks:
			lines.append(p.name)
		fi = item.ItemInfo(
			heading,
			lines,
			self.actions[activeActionId] + ':',
		)
		fi.setPositions()
		return fi


class RecruitmentHeaderItem(item.HeaderItem):
	def __init__(self):
		super().__init__('Recruitment')
		self.actions = [
			'Recruit all',
			'Recruit selected',
			'Next Recruits'
		]
	
	def getInfo(self, activeActionId):
		heading = 'Recruitment'
		lines = [
			'Recruits available: ' +str(10),
			]
		fi = item.ItemInfo(
			heading,
			lines,
			self.actions[activeActionId] + ':',
		)
		fi.setPositions()
		return fi
		

class RecruitmentSection(section.Section):
	
	listIndex = 0
	
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addFocus(RecruitmentHeaderItem())
		self._setCursorFocusIndex(0)

	def draw(self):
		super().draw()

	def setRecruits(self, recruits):
		del self.focuses[1:]
		for r in recruits[self.listIndex *10:self.listIndex *10 +10]:
			f = RecruitItem(r)
			self.addFocus(f)
			f.setPositions()
	
	def action(self, command):
		# for s in self.selection:
		
		if self.commands[command] == recruitSelected:
			self.game.recruited(list(map(lambda r: r.merc, self.selectedFocusesIndices)))
		elif dismissSelected:
			pass
		elif nextRecruits:
			pass
		elif previousRecruits:
			pass