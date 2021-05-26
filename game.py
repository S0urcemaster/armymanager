import math
from multiprocessing import Process
import sys, pygame
import random
import io
import locale
from datetime import datetime, timedelta

import lib
import gameenv
import color
import text
import layout
import section
from sections import header
import focus
import events
import merc
from sections.enemy import EnemySection
from sections.army import ArmySection
import sections.commands as commands
from sections.camp import CampSection
from sections.recruitment import RecruitmentSection

enemy = 0
frontline = 1
# commands = 2
camp = 2
recruitment = 3

class Game(Process):
	env: gameenv.GameEnv
	running: True
	screen = None
	sections = []
	focusedSection = None
	focusedSectionIndex = None
	firstnamesFile = "res/firstnames.txt"
	lastnamesFile = "res/familynames.txt"
	firstnames = []
	lastnames = []
	mercs = []
	
	def __init__(self, env: gameenv.GameEnv):
		super().__init__()
		locale.setlocale(locale.LC_TIME, "de_DE")
		self.env = env
		self.running = True

		with io.open(self.firstnamesFile, mode = "r", encoding = "utf-8") as file:
			self.firstnames = file.readlines()
		for i in range(len(self.firstnames)):
			self.firstnames[i] = self.firstnames[i].strip("\n")

		with io.open(self.lastnamesFile, mode = "r", encoding = "utf-8") as file:
			self.lastnames = file.readlines()
		for i in range(len(self.lastnames)):
			self.lastnames[i] = self.lastnames[i].strip("\n")

		pygame.init()
		pygame.key.set_repeat(250, 60)
		
		size = env.width, env.height
		self.screen = pygame.display.set_mode(size)
		
		text.Text.screen = self.screen
		section.Section.screen = self.screen
		focus.Focus.screen = self.screen
		
		mainLayout = layout.Layout(self.env.width, self.env.height)
		self.header = header.Header(mainLayout.getHeader())
		self.sections.append(EnemySection(mainLayout.getColumn(0)))
		self.border = section.Section(mainLayout.getColumn(1))
		self.sections.append(ArmySection(mainLayout.getColumn(2)))
		self.commands = commands.CommandsSection(mainLayout.getColumn(3))
		self.sections.append(CampSection(mainLayout.getColumn(4)))
		self.sections.append(RecruitmentSection(mainLayout.getColumn(5)))
		
		self.focusedSection = self.sections[recruitment]
		self.focusedSectionIndex = recruitment
		self.focusedSection.focus()
		
		self.gameEvents = events.Events()
		self.gameEvents.addEvent(events.Event(events.CLOCK_SECONDS, 1, self.gameEvents.currentTime))
		self.gameEvents.addEvent(events.Event(events.NEW_RECRUITS_EVENT, 1))
	
	def start(self):
		clock = pygame.time.Clock()
		self.sections[camp].initialMercs(self.makeMercs())
		while self.running:
			# evaluate player action
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_g: # print('up')
						self.focusedSection.keyUp()
					elif event.key == pygame.K_r: # print('down')
						self.focusedSection.keyDown()
					elif event.key == pygame.K_n: # print('left')
						if self.focusedSectionIndex >0:
							self.focusedSectionIndex -= 1
							self.focusedSection = self.sections[self.focusedSectionIndex]
							for s in self.sections: s.unfocus()
							self.focusedSection.focus()
							self.commands.previousState()
					elif event.key == pygame.K_t: # print('right')
						if self.focusedSectionIndex <len(self.sections) -1:
							self.focusedSectionIndex += 1
							self.focusedSection = self.sections[self.focusedSectionIndex]
							for s in self.sections: s.unfocus()
							self.focusedSection.focus()
							self.commands.nextState()
					elif event.key == pygame.K_SPACE: # print('space')
						self.focusedSection.space()
					elif event.key == pygame.K_TAB: # print('space')
						self.commands.tab()
					elif event.key == pygame.K_RETURN: # print('return')
						pass
					
			# evaluate game events
			for e in self.gameEvents.getRaisedEvents():
				if(e.name == events.CLOCK_SECONDS):
					self.gameEvents.renew(e, 1, self.gameEvents.currentTime)
					self.header.updateClock(self.gameEvents.currentTime.strftime("%A, %d. %B %Y - %H:%M:%S"))
				if(e.name == events.NEW_RECRUITS_EVENT):
					self.gameEvents.renew(e, 10)
					self.sections[recruitment].setRecruits(self.makeMercs())
					self.gameEvents.renew(e, 5)
			
			# draw frame
			self.screen.fill(color.middleGrey)
			self.header.draw()
			self.border.draw()
			self.commands.draw()
			for s in self.sections:
				s.draw()
			
			pygame.display.flip()
			dt = clock.tick(30)
			self.gameEvents.update(dt)

	def makeMercs(self):
		mercs = []
		for i in range(10):
			merci = merc.Merc()
			random.seed()
			merci.firstname = random.choice(self.firstnames)
			merci.lastname = random.choice(self.lastnames)
			merci.pay = random.randint(2, 16)
			merci.strength = random.randint(1, 255)
			merci.dexterity = random.randint(1, 255)
			merci.intelligence = random.randint(1, 255)
			merci.charisma = random.randint(1, 255)
			merci.confidence = random.randint(1, 255)
			merci.birthday = events.Event.current - timedelta(days = 365 *lib.bellAge() +random.randint(1, 365))
			# Perks:
			for i in range(3): # max 3 perks
				prob = random.randint(0, 11) # probability
				if i >= prob:
					while True: # no duplicates
						rand = random.randint(0, len(merc.perkList) -1)
						perk = merc.perkList[rand]
						found = False
						for p in merci.perks:
							if p.name == perk.name:
								found = True
						if found: continue
						merci.perks.append(perk)
						break
			mercs.append(merci)
		return mercs

	def exit(self):
		pygame.quit()
		sys.exit()

env = gameenv.GameEnv()
game = Game(env)
game.start()
