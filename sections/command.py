import pygame
import color
import section
import item
import text

class GameMenuCommands:
	welcome = 'Welcome'
	basicGameplay = 'Basic gameplay'
	about = 'About'
	quit = 'Quit game'

class EnemyCommands:
	spy = 'Spy'
	
class EnemyHeaderCommands:
	spy = 'spy'

class AssignmentCommands:
	choose = 'Choose assignment'

class AssignmentHeaderCommands:
	roll = 'Roll'

class FrontlineCommands:
	retreat = 'Retreat'

class FrontlineHeaderCommands:
	distribute = 'Distribute equally'

class CampCommands:
	train = 'Train next level'
	equip = 'Equip next level'
	infantry = 'Train as infantry'
	cavalry = 'Train as cavalry'
	archer = 'Train as archer'
	discharge = 'Discharge'

class CampHeaderCommands:
	equip = 'Equip all visible next level'

class RecruitCommands:
	recruit = 'Recruit'
	recruitAll = 'Recruit All'
	nextRecruits = 'Next Recruits'

class RecruitHeaderCommands:
	recruitAll = 'Recruit All'
	nextRecruits = 'Next Recruits'
	

class State:
	enemy = 0
	frontline = 1
	camp = 2
	recruitment = 3
	gameMenu = 4
	
	@staticmethod
	def getNext(s):
		if s <4: return s +1
		return s
	
	@staticmethod
	def getPrevious(s):
		if s >0: return s -1
		return s


class CommandItem(item.Item):
	def __init__(self, title:str):
		super().__init__(40)
		self.name = text.TextH(title)
	
	def draw(self):
		super().draw()
		self.name.draw()
	
	def setPositions(self):
		rect = self.name.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.name.setPosition(self.rect.x +rect.x, self.rect.y +rect.y -2)


class CommandsSection(section.Section):
	
	commands = []
	selectedCommand = None
	selectedCommandIndex = None
	focusInfo = None
	enemyOrAssignment = AssignmentCommands
	
	def __init__(self, rect):
		super().__init__(rect)
		self.state = State.gameMenu
		self.addItem(section.HeaderFocus('Commands'))
		self.__changeMenu(State.gameMenu)
		self.setFocusInfo(self.getFocusInfo())
	
	def draw(self):
		pygame.draw.rect(self.screen, color.brightGrey, self.items[self.selectedCommandIndex + 1].rect)
		self.focusInfo.draw()
		super().draw()
	
	def tab(self):
		if self.selectedCommandIndex <len(self.commands) -1:
			self.selectedCommandIndex += 1
			self.selectedCommand = self.commands[self.selectedCommandIndex]
		else:
			self.selectedCommandIndex = 0
			self.selectedCommand = self.commands[self.selectedCommandIndex]
		if self.state == State.gameMenu:
			self.setFocusInfo(self.getFocusInfo())
		
	def __changeMenu(self, sec):
		if sec == State.enemy:
			if self.headerSelected:
				if self.enemyOrAssignment == EnemyCommands:
					self.commands = self.__getCommands(EnemyHeaderCommands)
				else:
					self.commands = self.__getCommands(AssignmentHeaderCommands)
			else:
				self.commands = self.__getCommands(self.enemyOrAssignment) # classes are objects
		elif sec == State.frontline:
			if self.headerSelected:
				self.commands = self.__getCommands(FrontlineHeaderCommands)
			else:
				self.commands = self.__getCommands(FrontlineCommands)
		# elif(sec == State.details):
		# 	pass
		elif sec == State.camp:
			if self.headerSelected:
				self.commands = self.__getCommands(CampHeaderCommands)
			else:
				self.commands = self.__getCommands(CampCommands)
		elif sec == State.recruitment:
			if self.headerSelected:
				self.commands = self.__getCommands(RecruitHeaderCommands)
			else:
				self.commands = self.__getCommands(RecruitCommands)
		elif sec == State.gameMenu:
			self.commands = self.__getCommands(GameMenuCommands)
		
		# self.commands = list(filter(lambda v: not v.startswith('__') , commands))
		del self.items[1:]
		for c in self.commands:
			cf = CommandItem(c[1])
			self.addItem(cf)
		
		self.selectedCommandIndex = 0
		self.selectedCommand = self.commands[self.selectedCommandIndex]
	
	def __getCommands(self, t):
		"""return tuple (command variable, command title)"""
		commands = list(filter(lambda v: not v.startswith('__') , vars(t)))
		commands = list(map(lambda c: (c, getattr(t, c)), commands))
		return commands
		
	def nextState(self):
		self.state = State.getNext(self.state)
		self.__changeMenu(self.state)
		
	def previousState(self):
		self.state = State.getPrevious(self.state)
		self.__changeMenu(self.state)
	
	def setState(self, state):
		self.state = state
		self.__changeMenu(state)
	
	def gameMenu(self):
		self.setState(State.gameMenu)
		self.setFocusInfo(self.getFocusInfo())
		
	def gameMenuReturn(self, sec):
		self.setState(sec)
	
	def setAssignment(self):
		self.enemyOrAssignment = AssignmentCommands
		
	def setEnemy(self):
		self.enemyOrAssignment = EnemyCommands
		
	def setHeaderSelected(self, s, sec):
		self.headerSelected = s
		self.__changeMenu(sec)

	def setFocusInfo(self, info: item.ItemInfo):
		rect = self.rect
		rect.y = 500
		info.setPositions(rect)
		self.focusInfo = info
	
		