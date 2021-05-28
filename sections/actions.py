import pygame
import color
import text
import focus
import section

class ActionFocus(focus.Focus):
	def __init__(self, title:str):
		super().__init__(40)
		self.name = text.TextH(title)
		self.commands = []
	
	def draw(self):
		super().draw()
		self.name.draw()
	
	def setPositions(self):
		rect = self.name.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.name.setPosition(self.rect.x +rect.x, self.rect.y +rect.y)


class ActionsSection(section.Section):
	
	selectedAction = 0
	selectedItems = [] # menu needs to know about selection. Fed in selectionActive()
	
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addFocus(focus.HeaderFocus('Actions'))
		self.activeFocusChanged(None)
		rect = self.rect
		rect.y = 500
		rect.h = self.rect.h -rect.y +30
		focus.FocusInfo.rect = rect
	
	def draw(self):
		pygame.draw.rect(self.screen, color.brightGrey, self.focuses[self.selectedAction +1].rect)
		if self.activeFocus == None: # own infos
			self.focuses[self.selectedAction +1].getInfo([]).draw()
		else: # show active focus info
			self.activeFocus.getInfo(self.selectedAction).draw()
		super().draw()
	
	def activeFocusChanged(self, focus: focus.Focus):
		del self.focuses[1:]
		if len(self.selectedItems) >0:
			lst = list(self.selectedItems)
			self.activeFocus = lst[0]
			# intersection = set()
			intersection = set(lst[0].actions)
			for s in lst:
				intersection = intersection & set(s.actions)
			self.activeFocus.actions = intersection
			print(intersection)
		elif focus == None:
			self.addFocus(WelcomeActionFocus())
			self.addFocus(GameplayActionFocus())
			self.addFocus(AboutActionFocus())
			self.addFocus(QuitActionFocus())
			self.activeFocus = None
		else:
			self.activeFocus = focus
			for c in self.activeFocus.actions:
				cf = ActionFocus(c)
				self.addFocus(cf)
			
		self.selectedAction = 0
		
	def selectionActive(self, selection):
		self.selectedItems = selection
		
	def tab(self):
		if self.selectedAction <len(self.focuses) -2:
			self.selectedAction += 1
		else:
			self.selectedAction = 0
	
	def action(self, action):
		if action == 3:
			self.game.quit()
		
		
	


class WelcomeActionFocus(ActionFocus):
	def __init__(self):
		super().__init__('Welcome')
		self.commands = ['Welcome', 'Basic gameplay', 'About Army Manager', 'Quit game']
	def getInfo(self, activeCommand):
		fi = focus.FocusInfo(
			'Army Manager Prototype',
			[
				'Welcome to Army Manager',
				'Prototype! Aim of the game',
				'is getting a high score. You',
				'need to recruit mercenaries,',
				'train and equip them and',
				'send them to battle. If you',
				'win the battle you earn',
				'money from your client and',
				'can loot the battlefield. Your',
				'fame rises, too which gives',
				'you more recruits.',
				'Sooner or later, as the game',
				'progresses it will become',
				'harder to win conflicts',
				'which makes you run out of',
				'money or recruits. Your high',
				'score will be the maximum',
				'money gained.',
				'',
				'Use [TAB] to switch actions',
			]
		)
		fi.setPositions()
		return fi


class GameplayActionFocus(ActionFocus):
	def __init__(self):
		super().__init__('Basic gameplay')
		self.commands = ['Welcome', 'Basic gameplay', 'About Army Manager', 'Quit game']
	def getInfo(self, activeCommand):
		fi = focus.FocusInfo(
			'Basic gameplay',
			[
				'Press [ESC] to show game menu',
				'Use arrow keys to navigate',
				'Use [TAB] to toggle commands',
				'Use [SPACE] to select',
				'Use [RETURN] to execute command',
			]
		)
		fi.setPositions()
		return fi
	

class AboutActionFocus(ActionFocus):
	def __init__(self):
		super().__init__('About Army Manager')
		self.commands = ['Welcome', 'Basic gameplay', 'About Army Manager', 'Quit game']
	def getInfo(self, activeCommand):
		fi = focus.FocusInfo(
			'Army Manager Prototype',
			[
				'Developed by Sebastian Teister',
				'Mai 2021',
			]
		)
		fi.setPositions()
		return fi
	
	
class QuitActionFocus(ActionFocus):
	def __init__(self):
		super().__init__('Quit Game')
		self.commands = ['Welcome', 'Basic gameplay', 'About Army Manager', 'Quit game']
	def getInfo(self, activeCommand):
		fi = focus.FocusInfo(
			'Quit Game',
			[
				'Hit [RETURN] to quit'
			]
		)
		fi.setPositions()
		return fi