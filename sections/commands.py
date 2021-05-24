from collections import namedtuple, Iterable
import section
import focus
import text

class TrainEquipCommands:
	train = 'Train next level'
	equip = 'Equip next level'

class RecruitCommands:
	recruit = 'Recruit'
	recruitAll = 'Recruit All'
	nextRecruits = 'Next Recruits'


class State:
	opponent = 1
	army = 2
	equip = 3
	recruit = 4
	details = 5

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
		
		
class CommandsSection(section.Section):
	
	def __init__(self, rect):
		super().__init__(rect)
		self.state = State.recruit
		self.addFocus(section.HeaderFocus('Commands'))
		
	
	def draw(self):
		commands = []
		if(self.state == State.opponent):
			pass
		if(self.state == State.army):
			pass
		elif(self.state == State.details):
			pass
		elif(self.state == State.equip):
			commands = vars(TrainEquipCommands)
		elif(self.state == State.recruit):
			commands = vars(RecruitCommands)
			
		self.commands = filter(lambda v: not v.startswith('__') ,commands)
		
		del self.focuses[1:]
		for c in self.commands:
			cf = CommandFocus(c)
			self.addFocus(cf)
			cf.setPositions()
		super().draw()
		
