import pygame.draw

import section
import item
import text
import color
import merc
import events
import sections.camp as camp

RECRUIT = 'Recruit'
RECRUIT_SELECTED = 'Recruit selected'
DISMISS_SELECTED = 'Dismiss selected'
NEXT_RECRUITS = 'Next Recruits'
PREVIOUS_RECRUITS = 'Previous Recruits'
RECRUIT_VISIBLE = 'Recruit visible'

class RecruitmentHeaderItem(item.HeaderItem):
	def __init__(self):
		super().__init__('Recruitment')
		actions = [
			RECRUIT_VISIBLE,
			RECRUIT_SELECTED,
			NEXT_RECRUITS
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
			RECRUIT,
			NEXT_RECRUITS
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
		self.stats = section.SectionStats(0, self.rect)
		self.listMarker = section.ScrollBar(self.rect)
		

	def draw(self):
		super().draw()
		self.listMarker.draw()
		self.stats.draw()

	def setRecruits(self, recruits):
		del self.items[1:]
		for r in recruits[self.listIndex *10:self.listIndex *10 +10]:
			f = RecruitItem(r)
			self.addItem(f)
			f.setPositions()
		self.stats.update(len(recruits))
		self.listMarker.update(self.listIndex, len(recruits))
	
	def act(self, action):
		info = self.items[self.itemFocusIndex].info
		if info.actions[action] == RECRUIT:
			self.game.doRecruit(self.items[self.itemFocusIndex].soldier)
		elif info.actions[action] == RECRUIT_SELECTED:
			self.game.doNecruitSelected(list(map(lambda r: r.merc, self.selectedItemsIndices)))
		elif DISMISS_SELECTED:
			pass
		elif NEXT_RECRUITS:
			pass
		elif PREVIOUS_RECRUITS:
			pass