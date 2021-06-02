from datetime import datetime, timedelta

import merc as merci
import battlefield

CLOCK_SECONDS = "clock seconds"
NEW_RECRUITS_EVENT = "new recruits"
RECRUITED_EVENT = "recruited"
COMBAT_EVENT = "combat"
BATTLE_EVENT = "battle"

def combatEventToString(payload):
	merc: merci.Merc = payload[0][0]
	enemy: merci.Merc = payload[0][1]
	bfSector: battlefield.BfSector = payload[1]
	return f'[{merc.firstname} {merc.lastname} {merc.getPower()} wounds: {merc.wounds}]  ' \
	       f'[{enemy.firstname} {enemy.lastname} {enemy.getPower()} wounds: {enemy.wounds}]  '
	       # f''

def logEvent(name, seconds, payload):
	if payload.__class__.__name__ == 'tuple':
		if payload[0].__class__.__name__ == 'tuple':
			if payload[0][0].__class__.__name__ == 'Merc':
				print('Event created: ' +combatEventToString(payload))
			else:
				print('Event created: ', name, seconds, payload)
		else:
			print('Event created: ', name, seconds, payload)
	else:
		print('Event created: ', name, seconds, payload)


class Event:
	current = None
	def __init__(self, name, seconds, payload = None):
		self.name = name
		self.datetime = self.current +timedelta(seconds = seconds)
		self.payload = payload
		logEvent(name, seconds, payload)
	
	def renew(self, delta, payload = None):
		if payload != None:
			self.payload = payload
		self.datetime = self.current +timedelta(seconds = delta)
		logEvent(self.name, delta, self.payload)

class Events:
	
	currentTime = datetime(1618, 1, 1)
	events = []
	
	def __init__(self):
		Event.current = self.currentTime
	
	def renew(self, event, delta, payload = None):
		event.renew(delta, payload)
		
	def remove(self, event):
		self.events.remove(event)
	
	def addEvent(self, event):
		self.events.append(event)
	
	def getRaisedEvents(self):
		raised = []
		for e in self.events:
			if e.datetime <= self.currentTime:
				raised.append(e)
		return raised
	
	def update(self, millis):
		delta = timedelta(milliseconds = millis)
		self.currentTime = self.currentTime + delta
		Event.current = self.currentTime
	