import pygame
import color
import section
import focus
import text


class EnemyCommands:
	spy = 'Spy'


class FrontlineCommands:
	distribute = 'Distribute equally'
	retreat = 'Retreat'

class CampCommands:
	train = 'Train next level'
	equip = 'Equip next level'
	infantry = 'Train as infantry'
	cavalry = 'Train as cavalry'
	archer = 'Train as archer'
	discharge = 'Discharge'


class RecruitCommands:
	recruit = 'Recruit'
	recruitAll = 'Recruit All'
	nextRecruits = 'Next Recruits'


class State:
	enemy = 1
	frontline = 2
	camp = 3
	recruitment = 4
	# details = 5
	
	@staticmethod
	def getNext(s):
		if s <4: return s +1
		return s
	
	@staticmethod
	def getPrevious(s):
		if s >1: return s -1
		return s


class CommandFocus(focus.Focus):
	def __init__(self, title:str):
		super().__init__(40)
		self.name = text.TextH(title)
		self.commands = []
	
	def draw(self):
		super().draw()
		self.name.draw()
	
	def setPositions(self):
		rect = self.name.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.name.setPosition(self.rect.x +rect.x, self.rect.y +rect.y -2)


# class FocusInfo:


class CommandsSection(section.Section):
	
	commands = []
	selectedCommand = None
	selectedCommandIndex = None
	
	def __init__(self, rect):
		super().__init__(rect)
		self.state = State.recruitment
		self.addFocus(section.HeaderFocus('Commands'))
		self.sectionSelected(4)
	
	def draw(self):
		pygame.draw.rect(self.screen, color.brightGrey, self.focuses[self.selectedCommandIndex +1].rect)
		
		super().draw()
	
	def tab(self):
		if self.selectedCommandIndex <len(self.commands) -1:
			self.selectedCommandIndex += 1
			self.selectedCommand = self.commands[self.selectedCommandIndex]
		else:
			self.selectedCommandIndex = 0
			self.selectedCommand = self.commands[self.selectedCommandIndex]
		
	def sectionSelected(self, sec):
		if sec == State.enemy:
			self.commands = self.__getCommands(EnemyCommands)
		if sec == State.frontline:
			self.commands = self.__getCommands(FrontlineCommands)
		# elif(sec == State.details):
		# 	pass
		elif sec == State.camp:
			self.commands = self.__getCommands(CampCommands)
		elif sec == State.recruitment:
			self.commands = self.__getCommands(RecruitCommands)
		
		# self.commands = list(filter(lambda v: not v.startswith('__') , commands))
		del self.focuses[1:]
		for c in self.commands:
			cf = CommandFocus(c[1])
			self.addFocus(cf)
			cf.setPositions()
			
		self.selectedCommandIndex = 0
		self.selectedCommand = self.commands[self.selectedCommandIndex]
		
	def nextState(self):
		self.state = State.getNext(self.state)
		self.sectionSelected(self.state)
		
	def previousState(self):
		self.state = State.getPrevious(self.state)
		self.sectionSelected(self.state)
		
	def __getCommands(self, t):
		commands = list(filter(lambda v: not v.startswith('__') , vars(t)))
		commands = list(map(lambda c: (c, getattr(t, c)), commands))
		return commands
