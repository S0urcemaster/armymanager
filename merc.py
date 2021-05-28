import datetime

# class Trait:
# 	def __init__(self, name, value):
# 		self.__name

class Perk:
	
	def __init__(self, name, traits, factors, removable):
		self.name = name
		self.traits: [] = traits
		self.factors: [] = factors
		self.removable: bool = removable
	
	@staticmethod
	def makeList(names:[]):
		return list(map(lambda l: Perk(l[0], l[1], l[2], l[3]), names))

str = 'strength'
dex = 'dexterity'
ntl = 'intelligence'
con = 'confidence'
cha = 'charisma'
perkList = Perk.makeList([
	('Arthrosis', [str, con], [-0.25, -0.15], False),
	('Blessed', [str, dex, ntl, con, cha], [0.1, 0.1, 0.1, 0.1, 0.1], False),
	('Craftsman', [dex], [0.5], False),
	('Disability', [dex, con, cha], [-0.25, -0.25, -0.25], False),
	('Gifted', [dex, ntl], [0.25, 0.25], False),
	('Handsome', [cha], [0.5], False),
	('Injury', [str, con], [-0.25, -0.25], True),
	('Scholar', [ntl], [0.5], False),
	('Valor', [con], [0.5], False),
	('Berserker', [con, int], [0.5, -0.5], None),
])

class UnitType:
	captain = 'Captain'
	pikeman = 'Infantry'
	cavalry = 'Cavalry'
	musketeer = 'Musketeer'
	instructor = 'Instructor'
	doctor = 'Doctor'
	spy = 'Spy'
	recruit = 'Recruit'


class Experience:
	
	levels = [
		100, 200, 300, 600, 1200
	]
	
	def __init__(self, typ = UnitType.recruit, xp = 0):
		self.__typ = typ
		self.__xp = xp
	
	@property
	def level(self):
		if self.__xp <self.levels[0]: return 0
		for ix, l in enumerate(self.levels):
			if self.__xp>l: return ix +1
	
	@property
	def xp(self):
		return self.__xp
	@xp.setter
	def xp(self, x):
		self.__xp = x
	
	@property
	def typ(self):
		return self.__typ
	@typ.setter
	def typ(self, t):
		self.__typ = t
	
	def getLevel(self):
		if self.__xp <100: return 0
		elif self.__xp <200: return 1
		elif self.__xp <300: return 2
		elif self.__xp <600: return 3
		
	def levelUp(self):
		if self.__xp <100: self.__xp = 100
		elif self.__xp <200: self.__xp = 200
		elif self.__xp <300: self.__xp = 300
		elif self.__xp <600: self.__xp = 600
		
	def train(self, typ):
		self.__typ = typ
		self.__xp = 10


class Merc:
	def __init__(self):
		self.__firstname: str
		self.__lastname: str
		self.__birthday: datetime
		
		self.__strength: int
		self.__dexterity: int
		self.__intelligence: int
		self.__charisma: int
		self.__confidence: int

		# self.__typ = UnitType.recruit
		self.__experience = Experience()
		
		self.__perks = []

		self.__equipment = 0 # equipment level
		self.__pay: int # payment
		self.__asset = 0 # money in pockets
		
		self.__idle = False # is training or otherwise unavailable
		
	@property
	def firstname(self):
		return self.__firstname
	@firstname.setter
	def firstname(self, f):
		self.__firstname = f
	@property
	def lastname(self):
		return self.__lastname
	@lastname.setter
	def lastname(self, l):
		self.__lastname = l
	@property
	def birthday(self):
		return self.__birthday
	@birthday.setter
	def birthday(self, b):
		self.__birthday = b

	@property
	def strength(self):
		return self.__strength
	@strength.setter
	def strength(self, s):
		self.__strength = s
	@property
	def dexterity(self):
		return self.__dexterity
	@dexterity.setter
	def dexterity(self, d):
		self.__dexterity = d
	@property
	def intelligence(self):
		return self.__intelligence
	@intelligence.setter
	def intelligence(self, i):
		self.__intelligence = i
	@property
	def charisma(self):
		return self.__charisma
	@charisma.setter
	def charisma(self, c):
		self.__charisma = c
	@property
	def confidence(self):
		return self.__confidence
	@confidence.setter
	def confidence(self, c):
		self.__confidence = c
	
	# @property
	# def typ(self):
	# 	return self.__typ
	# @typ.setter
	# def typ(self, t):
	# 	self.__typ = t
	@property
	def xp(self):
		return self.__experience
	@xp.setter
	def xp(self, e):
		self.__experience = e
	@property
	def level(self):
		return self.__experience.level
	@property
	def xpTyp(self):
		return self.__experience.typ
	
	@property
	def perks(self):
		return self.__perks
	@perks.setter
	def perks(self, p):
		self.__perks = p
	
	@property
	def pay(self):
		return self.__pay
	@pay.setter
	def pay(self, p):
		self.__pay = p

	@property
	def asset(self):
		return self.__asset
	@asset.setter
	def asset(self, a):
		self.__asset = a

	# @property
	# def (self):
	# 	return self.__
	# @.setter
	# def (self, ):
	# 	self.__ =
	
	def getAge(self, date: datetime):
		return int((date - self.__birthday).total_seconds() // (60 *60 *24 *365))
	