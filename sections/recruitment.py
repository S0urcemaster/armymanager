import pygame.draw

import section
import item
import text
import color
import merc
import events
import sections.camp as camp

recruitSelected = 'Recruit selected'
dismissSelected = 'Dismiss selected'
nextRecruits = 'Next Recruits'
previousRecruits = 'Previous Recruits'

class RecruitmentHeaderItem(item.HeaderItem):
	def __init__(self):
		super().__init__('Recruitment')
		actions = [
			'Recruit all',
			'Recruit selected',
			'Next Recruits'
		]
		self.info = item.ItemInfo(
			'Recruitment',
			[
				'Recruits available: ' +str(10),
			], actions
		)

class RecruitItem(camp.MercItem):
	def __init__(self, recruit: merc.Merc):
		super().__init__(recruit)
		actions = [
			'Recruit',
			'Next Recruits'
		]
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
		

class RecruitmentSection(section.Section):
	
	listIndex = 0
	
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addItem(RecruitmentHeaderItem())
		self._setItemFocusIndex(0)

	def draw(self):
		super().draw()

	def setRecruits(self, recruits):
		del self.items[1:]
		for r in recruits[self.listIndex *10:self.listIndex *10 +10]:
			f = RecruitItem(r)
			self.addItem(f)
			f.setPositions()
	
	def action(self, action):
		# for s in self.selection:
		
		if self.actions[action] == recruitSelected:
			self.game.recruited(list(map(lambda r: r.merc, self.selectedItemsIndices)))
		elif dismissSelected:
			pass
		elif nextRecruits:
			pass
		elif previousRecruits:
			pass