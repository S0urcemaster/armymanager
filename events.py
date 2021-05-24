from datetime import datetime, timedelta

CLOCK_SECONDS = "clock seconds"
NEW_RECRUITS_EVENT = "new recruits"

class Event:
	current = None
	def __init__(self, name, seconds, payload = None):
		self.name = name
		self.datetime = self.current +timedelta(seconds = seconds)
		self.payload = payload
	
	def renew(self, delta, payload):
		self.datetime = self.current +timedelta(seconds = delta)
		self.payload = payload

class Events:
	
	currentTime = datetime(1618, 1, 1)
	events = []
	
	def __init__(self):
		Event.current = self.currentTime
	
	def renew(self, event, delta, payload = 0):
		event.renew(delta, payload)
		
	def pop(self, event):
		self.events.pop(event)
	
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
	