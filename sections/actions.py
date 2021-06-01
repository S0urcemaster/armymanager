import pygame
import color
import text
import item
import section

class ActionItem(item.Item):
	def __init__(self, title:str):
		super().__init__(40)
		self.name = text.TextH(title)
	
	def draw(self):
		super().draw()
		self.name.draw()
	
	def setPositions(self):
		rect = self.name.text.get_rect(center = (self.rect.w //2, self.rect.h //2))
		self.name.setPosition(self.rect.x +rect.x, self.rect.y +rect.y)


class ActionsSection(section.Section):
	
	selectedAction = 0
	"""which is selected with tab"""
	
	def __init__(self, rect, game):
		super().__init__(rect, game)
		self.addItem(item.HeaderItem('Actions'))
		self.activeItemChanged(None)
		# self.activeItem = None
		rect = self.rect
		rect.y = 500
		rect.h = self.rect.h -rect.y +30
		item.ItemInfo.rect = rect
	
	def draw(self):
		# if len(self.items) >1:
		pygame.draw.rect(self.screen, color.brightGrey, self.items[self.selectedAction + 1].rect)
		if self.activeItem == None: # own infos
			self.items[self.selectedAction + 1].getInfo([]).draw()
		else: # show active focus info
			self.activeItem.getInfo(self.selectedAction).draw()
		super().draw()
	
	def activeItemChanged(self, item: item.Item):
		del self.items[1:]
		if item == None: # item is none when in menu mode
			self.addItem(WelcomeActionItem())
			self.addItem(GameplayActionItem())
			self.addItem(AboutActionItem())
			self.addItem(QuitActionItem())
			self.addItem(Recruits100ActionItem())
			self.activeItem = None
		else:
			for c in item.info.actions:
				# the active items actions become this sections' items
				cf = ActionItem(c)
				self.addItem(cf)
			self.activeItem = item
		if self.selectedAction >len(self.items):
			self.selectedAction = 0
		
	def tab(self):
		if self.selectedAction <len(self.items) -2:
			self.selectedAction += 1
		else:
			self.selectedAction = 0
	
	def up(self):
		if self.selectedAction >0:
			self.selectedAction -= 1
	
	def down(self):
		if self.selectedAction <len(self.items) -2:
			self.selectedAction += 1
	
	def selectionActive(self, selection):
		if len(selection) >1: # adjust actions list towards selected focuses' actions intersection
			lst = list(selection)
			self.activeItem = lst[0]
			# intersection = set()
			intersection = set(lst[0].info.actions)
			for s in lst:
				intersection = intersection & set(s.info.actions)
			self.activeItem.info.actions = list(intersection)
	
	def act(self, action):
		if action == 3:
			self.game.quit()
		if action == 4:
			self.game.doMake100Recruits()


class WelcomeActionItem(ActionItem):
	def __init__(self):
		super().__init__('Welcome')
		self.info = item.ItemInfo(
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


class GameplayActionItem(ActionItem):
	def __init__(self):
		super().__init__('Basic gameplay')
		self.info = item.ItemInfo(
			'Basic gameplay',
			[
				'Press [ESC] to show game menu',
				'Use arrow keys to navigate',
				'Use [TAB] to toggle commands',
				'Use [SPACE] to select',
				'Use [RETURN] to execute command',
			]
		)
	

class AboutActionItem(ActionItem):
	def __init__(self):
		super().__init__('About Army Manager')
		self.info = item.ItemInfo(
			'Army Manager Prototype',
			[
				'Developed by Sebastian Teister',
				'Mai 2021',
			]
		)
	
	
class QuitActionItem(ActionItem):
	def __init__(self):
		super().__init__('Quit Game')
		self.info = item.ItemInfo(
			'Quit Game',
			[
				'Hit [RETURN] to quit'
			]
		)
	
	
class Recruits100ActionItem(ActionItem):
	def __init__(self):
		super().__init__('Make 100 Recruits')
		self.info = item.ItemInfo(
			'Test it!',
			[
				'Hit [RETURN] to make'
			]
		)