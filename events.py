from datetime import datetime, timedelta

import merc as merci
import battlefield

CLOCK_SECONDS = "clock seconds"
NEW_RECRUITS_EVENT = "new recruits"
RECRUITED_EVENT = "recruited"
COMBAT_EVENT = "combat"
BATTLE_EVENT = "battle"


class Event:
	
	pointInTime = None
	
	def __init__(self, name, seconds, payload = None):
		self.name = name
		self.datetime = self.pointInTime + timedelta(seconds = seconds)
		self.payload = payload
		logEvent(name, seconds, payload, 'created')
	
	def renew(self, delta, payload = None):
		if payload != None:
			self.payload = payload
		self.datetime = self.pointInTime + timedelta(seconds = delta)
		logEvent(self.name, delta, self.payload, 'renewed')


class Events:
	
	gameTime = datetime(1618, 1, 1)
	events = []
	
	def __init__(self):
		Event.pointInTime = self.gameTime
	
	def renew(self, event, delta, payload = None):
		event.renew(delta, payload)
		
	def remove(self, event):
		self.events.remove(event)
	
	def addEvent(self, event):
		self.events.append(event)
	
	def getRaisedEvents(self):
		raised = []
		for e in self.events:
			if e.datetime <= self.gameTime:
				raised.append(e)
		return raised
	
	def update(self, millis):
		delta = timedelta(milliseconds = millis)
		self.gameTime = self.gameTime + delta
		Event.pointInTime = self.gameTime


def combatEventToString(payload):
	merc: merci.Merc = payload[0][0]
	enemy: merci.Merc = payload[0][1]
	bfSector: battlefield.BfSector = payload[1]
	return f'[{merc.firstname} {merc.lastname} {merc.getPower()} wounds: {merc.wounds}]  ' \
	       f'[{enemy.firstname} {enemy.lastname} {enemy.getPower()} wounds: {enemy.wounds}]  '


def logEvent(name, seconds, payload, text):
	if payload.__class__.__name__ == 'tuple':
		if payload[0].__class__.__name__ == 'tuple':
			if payload[0][0].__class__.__name__ == 'Merc':
				print(f'Event {text}: ' +combatEventToString(payload))
			else:
				print(f'Event {text}: ', name, seconds, payload)
		else:
			print(f'Event {text}: ', name, seconds, payload)
	else:
		print(f'Event {text}: ', name, seconds, payload)
