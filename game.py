from multiprocessing import Process
import sys, pygame
import locale
from threading import Lock

import lib
import gameenv
import color
import text
import layout
import section
from sections import header
import item
import events
import merc
from sections.assignment import AssignmentSection
from sections.troups import TroupsSection
import sections.actions as actions
from sections.camp import CampSection
from sections.recruitment import RecruitmentSection
from army import Army
from assignments import Assignment
import scenarios

assignment = 0
troups = 1
camp = 2
recruitment = 3


class Game(Process):
	# static fields
	env: gameenv.GameEnv
	running: True
	screen = None # pygame screen
	sections = [] # columns on the playfield
	focusedSection = None # cursor is in this column
	focusedSectionIndex = None
	
	recruits = [] # all available recruits
	mercs = [] # all recruited mercenaries
	army = Army()
	
	lock = Lock()
	
	def __init__(self, env: gameenv.GameEnv):
		super().__init__()
		locale.setlocale(locale.LC_TIME, "de_DE")
		self.env = env
		self.running = True
		
		lib.readNames()
	
		self.background = pygame.image.load('res/alu.jpg')
		
		pygame.init()
		
		# pygame.key.set_repeat(250, 60)
		size = env.width, env.height
		
		self.screen = pygame.display.set_mode(size)
		text.Text.screen = self.screen
		section.Section.screen = self.screen
		item.Item.screen = self.screen
		section.SectionStats.screen = self.screen
		section.ScrollBar.screen = self.screen
		
		mainLayout = layout.Layout(self.env.width, self.env.height)
		self.header = header.Header(mainLayout.getHeader(), self)
		self.sections.append(AssignmentSection(mainLayout.getColumn(0), self))
		self.border = section.Section(mainLayout.getColumn(1), self)
		self.sections.append(TroupsSection(mainLayout.getColumn(2), self))
		self.actions = actions.ActionsSection(mainLayout.getColumn(3), self)
		self.sections.append(CampSection(mainLayout.getColumn(4), self))
		self.sections.append(RecruitmentSection(mainLayout.getColumn(5), self))
		
		self.focusedSection = self.sections[recruitment]
		self.focusedSectionIndex = recruitment
		self.focusedSection.focus()
		
		self.gameEvents = events.Events()
		self.gameEvents.addEvent(events.Event(events.CLOCK_SECONDS, 1, self.gameEvents.currentTime))
		self.gameEvents.addEvent(events.Event(events.NEW_RECRUITS_EVENT, 1))
	
	def start(self):
		clock = pygame.time.Clock()
		self.mercs = lib.make10Mercs()
		self.sections[camp].update(self.mercs)
		while self.running:
			# evaluate player action
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_g: # UP
						focus = self.focusedSection.keyUp()
						self.actions.activeItemChanged(focus)
						
					elif event.key == pygame.K_r: # DOWN
						focus = self.focusedSection.keyDown()
						self.actions.activeItemChanged(focus)
						
					elif event.key == pygame.K_n: # LEFT
						if self.focusedSectionIndex >0:
							self.focusedSectionIndex -= 1
							self.focusedSection = self.sections[self.focusedSectionIndex]
							for s in self.sections: s.unfocus()
							focus = self.focusedSection.focus()
							self.actions.activeItemChanged(focus)
							
					elif event.key == pygame.K_t: # RIGHT
						if self.focusedSectionIndex <len(self.sections) -1:
							self.focusedSectionIndex += 1
							self.focusedSection = self.sections[self.focusedSectionIndex]
							for s in self.sections: s.unfocus()
							focus = self.focusedSection.focus()
							self.actions.activeItemChanged(focus)
							
					elif event.key == pygame.K_SPACE: # SPACE
						selection = self.focusedSection.space()
						if len(selection) >0:
							self.actions.selectionActive(selection)
							
					elif event.key == pygame.K_TAB or event.key == pygame.K_s: # TAB
						self.actions.tab()
						
					elif event.key == pygame.K_l:
						self.actions.up()
					elif event.key == pygame.K_a:
						self.actions.down()
						
					elif event.key == pygame.K_RETURN or event.key == pygame.K_h: # RETURN
						if self.actions.activeItem == None:
							self.actions.act(self.actions.selectedAction)
						else:
							self.focusedSection.act(self.actions.selectedAction)
						
					elif event.key == pygame.K_ESCAPE: # ESCAPE
						self.actions.activeItemChanged(None)
					
			# evaluate game events
			for e in self.gameEvents.getRaisedEvents():
				if(e.name == events.CLOCK_SECONDS):
					self.gameEvents.renew(e, 1, self.gameEvents.currentTime)
					self.header.updateClock(self.gameEvents.currentTime.strftime("%A, %d. %B %Y - %H:%M:%S"))
					
				if(e.name == events.NEW_RECRUITS_EVENT):
					# self.gameEvents.renew(e, 10)
					self.recruits.append(lib.makeRecruit())
					self.sections[recruitment].update(self.recruits)
					self.gameEvents.renew(e, 1)
					
				# if(e.name == events.RECRUITED_EVENT):
				# 	self.sections[recruitment].setRecruits(self.recruits)
				# 	self.sections[camp].update(self.mercs)
					# self.gameEvents.remove(e)
			
			# draw frame
			# self.screen.fill(color.middleGrey)
			self.screen.blit(self.background, pygame.Rect(0, 0, 0, 0))
			self.header.draw()
			self.border.draw()
			self.actions.draw()
			for s in self.sections:
				s.draw()
			
			pygame.display.flip()
			dt = clock.tick(30)
			self.header.updateFps(str(dt))
			self.gameEvents.update(dt) # update game's current time

	def exit(self):
		self.running = False
		pygame.quit()
		sys.exit()
		
	# callbacks
	
	def doRecruit(self, recruit: merc.Merc):
		# self.lock.acquire()
		# try:
		self.recruits.remove(recruit) # throws 'not in list'
		self.mercs.append(recruit)
		self.gameEvents.addEvent(events.Event(events.RECRUITED_EVENT, 0.001))
		self.sections[recruitment].update(self.recruits)
		self.sections[camp].update(self.mercs)
		# except:
		# 	pass
		# self.lock.release()
	
	def doRecruitSelected(self, recruits):
		"""Called from recruitment when selection is accepted"""
		print(recruits)
	
	
	def doTrain(self, merc:merc.Merc, typ:merc.UnitType):
		merc.xp.typ = typ
		self.sections[camp].update(self.mercs)
	
	def selectThisAssignment(self, assignment:Assignment):
		self.army = Army(assignment.sectors)
		self.sections[troups].update(self.army)
		
	def battle(self):
		pass
		
	def put10Pikemen(self, sectorIndex):
		move = []
		for m in self.mercs:
			if m.xp.typ == merc.UnitType.pikeman:
				move.append(m)
			if len(move) == 10: break
		for m in move:
			self.army.sectors[sectorIndex].pikemen.append(m)
			self.mercs.remove(m)
		self.sections[troups].update(self.army)
		self.sections[camp].update(self.mercs)
		# update info changes:
		self.actions.activeItemChanged(self.sections[troups].items[self.sections[troups].itemFocusIndex])
		
	def put10CavalryMen(self, sectorIndex):
		pass
		
	def put10Musketeers(self, sectorIndex):
		pass
		
	def removeAll(self, sectorIndex):
		pass
		
	# game menu
	
	def quit(self):
		exit()
	
	# test

	def doMake100Recruits(self):
		self.recruits.extend(lib.make100Recruits())
	
	def initPfullingScenario(self):
		scene = scenarios.PfullingScenario()
		self.sections[assignment].setAssignment(scene.assignment)

env = gameenv.GameEnv()
game = Game(env)
game.start()
