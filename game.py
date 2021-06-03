import sys, pygame
import locale
import random

import lib
import gameenv
import text
import layout
import section
from sections import header
import item
import events
import merc
from sections.assignment import AssignmentSection
from sections.troops import TroopsSection
import sections.actions as actions
from sections.camp import CampSection
from sections.recruitment import RecruitmentSection
from army import Army
from assignments import Assignment
import scenarios
import battlefield
import color


ASSIGNMENT = 0
TROOPS = 1
CAMP = 2
RECRUITMENT = 3


class Game():
	# static fields
	env: gameenv.GameEnv
	running: True
	screen = None # pygame screen
	sections = [] # columns on the playfield
	focusedSection = None # cursor is in this column
	focusedSectionIndex = None
	
	recruits = []
	"""All available recruits"""
	mercs = []
	"""All recruited mercenaries"""
	army = Army()
	"""Player's army"""
	assignment = None
	"""Current assignment"""
	battlefield: battlefield.Battlefield
	"""Where the action takes place"""
	
	def __init__(self, env: gameenv.GameEnv):
		locale.setlocale(locale.LC_TIME, "de_DE")
		self.env = env
		self.running = True
		
		lib.readNames()
	
		self.background = pygame.image.load('res/alu.jpg')
		
		pygame.init()
		
		# pygame.key.set_repeat(250, 60)
		
		self.screen = pygame.display.set_mode((env.width, env.height))
		
		text.Text.screen = self.screen
		section.Section.screen = self.screen
		item.Item.screen = self.screen
		section.SectionStats.screen = self.screen
		section.ScrollBar.screen = self.screen
		
		mainLayout = layout.Layout(self.env.width, self.env.height)
		
		self.header = header.Header(mainLayout.getHeader(), self)
		self.sections.append(AssignmentSection(mainLayout.getColumn(0), self))
		self.border = section.Section(mainLayout.getColumn(1), self)
		self.sections.append(TroopsSection(mainLayout.getColumn(2), self))
		self.actions = actions.ActionsSection(mainLayout.getColumn(3), self)
		self.sections.append(CampSection(mainLayout.getColumn(4), self))
		self.sections.append(RecruitmentSection(mainLayout.getColumn(5), self))
		
		self.focusedSection:section.Section = self.sections[RECRUITMENT]
		"""The section that has focus"""
		self.focusedSectionIndex = RECRUITMENT
		"""Index of the focused section"""
		self.focusedSection.focus()
		
		self.gameEvents = events.Events()
		
		self.gameEvents.addEvent(events.Event(events.CLOCK_SECONDS, 1, self.gameEvents.gameTime))
		self.gameEvents.addEvent(events.Event(events.NEW_RECRUITS_EVENT, 1))
	
	
	def start(self):
		
		clock = pygame.time.Clock()
		
		self.mercs = lib.make10Recs()
		self.sections[CAMP].update(self.mercs)
		
		while self.running:
			
			# evaluate player action
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					self.exit()
					
				if event.type == pygame.KEYDOWN:
					
					if event.key == pygame.K_g or event.key == pygame.K_UP: # UP - row up
						focus = self.focusedSection.keyUp()
						self.actions.activeItemChanged(focus)
						
					elif event.key == pygame.K_r or event.key == pygame.K_DOWN: # DOWN - row down
						focus = self.focusedSection.keyDown()
						self.actions.activeItemChanged(focus)
						
					elif event.key == pygame.K_n or event.key == pygame.K_LEFT: # LEFT - column left
						if self.focusedSectionIndex >0:
							self.focusedSectionIndex -= 1
							self.focusedSection = self.sections[self.focusedSectionIndex]
							for s in self.sections: s.unfocus()
							focus = self.focusedSection.focus()
							self.actions.activeItemChanged(focus)
							
					elif event.key == pygame.K_t or event.key == pygame.K_RIGHT: # RIGHT - column right
						if self.focusedSectionIndex <len(self.sections) -1:
							self.focusedSectionIndex += 1
							self.focusedSection = self.sections[self.focusedSectionIndex]
							for s in self.sections: s.unfocus()
							focus = self.focusedSection.focus()
							self.actions.activeItemChanged(focus)
							
					elif event.key == pygame.K_SPACE: # SPACE - select item(s)
						selection = self.focusedSection.space()
						if len(selection) >0:
							self.actions.selectionActive(selection)
							
					elif event.key == pygame.K_TAB or event.key == pygame.K_s: # TAB - move actions
						self.actions.tab()
						
					elif event.key == pygame.K_l: # also move actions
						self.actions.up()
					elif event.key == pygame.K_a:
						self.actions.down()
						
					elif event.key == pygame.K_RETURN or event.key == pygame.K_h: # RETURN - activate action
						if self.actions.activeItem == None:
							self.actions.act(self.actions.selectedAction)
						else:
							self.focusedSection.act(self.actions.selectedAction)
						
					elif event.key == pygame.K_ESCAPE: # ESCAPE - show menu
						self.actions.activeItemChanged(None)
					
					
			# evaluate game events
			
			for e in self.gameEvents.getRaisedEvents():
				if e.name == events.CLOCK_SECONDS:
					self.header.updateClock(self.gameEvents.gameTime.strftime("%A, %d. %B %Y - %H:%M:%S"))
					
				elif e.name == events.NEW_RECRUITS_EVENT:
					self.recruits.append(lib.makeRecruit())
					self.sections[RECRUITMENT].update(self.recruits)
					e.renew(random.randint(1, 20) /10)
				
				elif e.name == events.BATTLE_EVENT:
					pass
				
				elif e.name == events.COMBAT_EVENT:
					pair = e.payload[0]
					sector = e.payload[1]
					result = self.rollFight(pair, sector)
					if result == True: # fight still going
						e.renew(lib.oneToTwoSeconds())
						pass
					elif result.__class__.__name__ == 'tuple': # new pair
						self.gameEvents.remove(e)
						self.gameEvents.addEvent(events.Event(events.COMBAT_EVENT, lib.oneToTwoSeconds(), (result, e.payload[1])))
					else: # fight settled
						arm, enemy = self.battlefield.getArmies()
						self.sections[TROOPS].update(arm)
						self.assignment.army = enemy
						self.sections[ASSIGNMENT].setAssignment(self.assignment)
						self.gameEvents.remove(e)
					# self.sections[troops].flash(e.payload[2], result[0])
					# self.sections[assignment].flash(e.payload[2], result[1])
					
					
			# draw frame
			
			self.screen.blit(self.background, pygame.Rect(0, 0, 0, 0))
			self.header.draw()
			self.border.draw()
			self.actions.draw()
			for s in self.sections:
				s.draw()
			
			pygame.display.flip()
			
			frameTime = clock.tick(30)
			
			self.header.updateFps(str(frameTime))
			self.gameEvents.update(frameTime) # update game's current time


	def exit(self):
		self.running = False
		pygame.quit()
		sys.exit()
		
		
	# --- callbacks ---
	
	def doRecruit(self, recruit: merc.Merc):
		self.recruits.remove(recruit) # throws 'not in list'
		self.mercs.append(recruit)
		self.gameEvents.addEvent(events.Event(events.RECRUITED_EVENT, 0.001))
		self.sections[RECRUITMENT].update(self.recruits)
		self.sections[CAMP].update(self.mercs)
	
	
	def doRecruitSelected(self, recruits):
		"""Called from recruitment when selection is accepted"""
		print(recruits)
	
	
	def doTrain(self, merc:merc.Merc, typ:merc.UnitType):
		merc.xp.typ = typ
		self.sections[CAMP].update(self.mercs)
	
	
	def selectThisAssignment(self, assign:Assignment):
		self.army = Army(assign.sectors)
		self.assignment = assign
		self.sections[TROOPS].update(self.army)
		# build enemy troops:
		army = lib.buildLowArmy(1, 10)
		assign.army = army
		self.sections[ASSIGNMENT].setAssignment(assign)
		
		
	def battle(self):
		self.battlefield = battlefield.Battlefield(self.army, self.assignment.army)
		# self.gameEvents.addEvent(events.Event(events.BATTLE_EVENT, 1))
		self.conflict()
		
		
	def conflict(self):
		for s in self.battlefield.sectors:
			pikemen = s.conflicPikemen()
			if pikemen:
				for p in pikemen:
					self.gameEvents.addEvent(events.Event(events.COMBAT_EVENT, lib.oneToTwoSeconds(), (p, s)))
			cavalryMen = s.conflictCavalryMen()
			if cavalryMen:
				for c in cavalryMen:
					self.gameEvents.addEvent(events.Event(events.COMBAT_EVENT, lib.oneToTwoSeconds(), (c, s)))
			musketeers = s.conflictMusketeers()
			if musketeers:
				for m in musketeers:
					self.gameEvents.addEvent(events.Event(events.COMBAT_EVENT, lib.oneToTwoSeconds(), (m, s)))
			
	
	def rollFight(self, pair, sector):
		merc = pair[0]
		enem = pair[1]
		powMerc = merc.getPower() -merc.wounds *10
		powEnem = enem.getPower() -enem.wounds *10
		powMerc *= merc.getAdvantage(enem.xp.typ) *100 # make int
		powEnem *= merc.getAdvantage(merc.xp.typ) *100
		powMerc *= int((1/ (merc.wounds +2)) *10)
		powEnem *= int((1/ (merc.wounds +2)) *10)
		hitMerc = random.randint(0, powMerc) //powEnem
		hitEnem = random.randint(0, powEnem) //powMerc
		
		merc.wounds += hitEnem #+random.randint(0, 1)
		enem.wounds += hitMerc #+random.randint(0, 1)
		
		res = self.getFlashColor(merc, enem)
		
		self.sections[TROOPS].items[1].flash(res[0], res[1])
		self.sections[ASSIGNMENT].items[1].flash(res[2], res[3])
		
		
		kia = False
		if merc.wounds >=4:
			merc.wounds = 4
			kia = True
		if enem.wounds >=4:
			enem.wounds = 4
			kia = True
		if kia:
			newPair = sector.kia(pair)
			if newPair:
				return newPair
			return False
		return True
	
	
	def getFlashColor(self, merc, enem):
		mercTime = 0
		mercColor = color.white
		if merc.wounds >0:
			mercColor = color.gold
			mercTime = 2
			if merc.wounds >1:
				mercColor = color.orange
				mercTime = 4
				if merc.wounds >2:
					mercColor = color.red
					mercTime = 8
					if merc.wounds >3:
						mercColor = color.black
						mercTime = 16
		enemyColor = color.white
		enemTime = 0
		if enem.wounds >0:
			enemyColor = color.gold
			enemTime = 2
			if enem.wounds >1:
				enemyColor = color.orange
				enemTime = 4
				if enem.wounds >2:
					enemyColor = color.red
					enemTime = 8
					if enem.wounds >3:
						enemyColor = color.black
						enemTime = 16
		return (mercTime, mercColor, enemTime, enemyColor)
		
	
	
	def checkSurrender(self):
		# count wounds
		troops = lib.countWounds(self.army)
		enemy = lib.countWounds(self.assignment.army)
		troopsLen = len(self.assignment.army.getTotalMercs())
		enemyLen = len(self.assignment.army.getTotalMercs())
		if troops //2 > troopsLen and enemy //2 <=enemyLen: # enemy won
			return troops
		elif enemy //2 > enemyLen and troops //2 <=troopsLen: # troops won
			return enemy
		elif troops == troopsLen *4 and enemy < enemyLen *4: # all troops dead
			return troops
		elif enemy == enemyLen *4 and troops < troopsLen *4: # all enemy dead
			return enemy
		else: return None # all dead?
		
	def put10Pikemen(self, sectorIndex):
		move = []
		for m in self.mercs:
			if m.xp.typ == merc.UnitType.pikeman:
				move.append(m)
			if len(move) == 10: break
		for m in move:
			self.army.sectors[sectorIndex].pikemen.append(m)
			self.mercs.remove(m)
		self.sections[TROOPS].update(self.army)
		self.sections[CAMP].update(self.mercs)
		# update info changes:
		self.actions.activeItemChanged(self.sections[TROOPS].items[self.sections[TROOPS].itemFocusIndex])
		
	def put10CavalryMen(self, sectorIndex):
		pass
		
	def put10Musketeers(self, sectorIndex):
		pass
		
	def removeAll(self, sectorIndex):
		pass
		
	# --- game menu ---
	
	def quit(self):
		exit()
	
	# --- test ---

	def doMake100Recruits(self):
		self.recruits.extend(lib.make100Recs())
	
	def initPfullingScenario(self):
		scene = scenarios.PfullingScenario()
		self.army = scene.army
		self.assignment = scene.assignment
		self.sections[ASSIGNMENT].setAssignment(scene.assignment)
		self.sections[TROOPS].update(scene.army)
	
	def initOfenhaufnScenario(self):
		scene = scenarios.OfenhaufnScenario()
		self.army = scene.army
		self.assignment = scene.assignment
		self.sections[ASSIGNMENT].setAssignment(scene.assignment)
		self.sections[TROOPS].update(scene.army)


env = gameenv.GameEnv()
game = Game(env)
game.start()
