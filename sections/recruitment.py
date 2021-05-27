import pygame.draw

import section
import focus
import text
import color
import merc
import events

class RecruitFocus(focus.Focus):
	def __init__(self, recruit: merc.Merc):
		super().__init__(85)
		self.recruit:merc.Merc = recruit
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


class RecruitmentSection(section.Section):
	def __init__(self, rect):
		super().__init__(rect)
		self.addFocus(section.HeaderFocus('Recruitment'))
		self.setCurrentFocusIndex(0)

	def draw(self):
		super().draw()

	def setRecruits(self, recruits):
		del self.focuses[1:]
		for r in recruits:
			f = RecruitFocus(r)
			self.addFocus(f)
			f.setPositions()
	
	def getFocusInfo(self):
		if (self.currentFocusIndex == 0):
			heading = "Recruitment"
			lines = [
				'Recruits: x'
			]
		else:
			recruit = self.focuses[self.currentFocusIndex].recruit
			heading = recruit.firstname +' ' +recruit.lastname
			lines = [
				'Age: ' +str(recruit.getAge(events.Event.current)),
				'Training: ' +recruit.xp.typ,
				'Experience: ' +str(recruit.xp.xp),
				'Pay: ' +str(recruit.pay),
				'Pockets: ' +str(recruit.asset),
				'Strength: ' +str(recruit.strength),
				'Dexterity: ' +str(recruit.dexterity),
				'Intelligence: ' +str(recruit.intelligence),
				'Charisma: ' +str(recruit.charisma),
				'Confidence: ' +str(recruit.confidence),
			]
			for p in recruit.perks:
				lines.append(p.name)
				
		return focus.FocusInfo(heading, lines)