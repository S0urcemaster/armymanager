import random
import numpy as np
from scipy.stats import norm
import io
from datetime import datetime, timedelta
import math

import merc
import events
import army as arm

firstnames = [] # Mercenaries randomly made of
lastnames = []

def bellAge() -> []:
    x = [random.randint(1, 100) for i in range(100)]
    mean = np.mean(x)
    sd = np.std(x)
    pdf = list(map(lambda x: ((x-18) /2) +18, (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)))
    return round(pdf[random.randint(0, 99)])


def readNames():
    with io.open("res/firstnames.txt", mode = "r", encoding = "utf-8") as file:
        global firstnames
        firstnames = file.readlines()
    for i in range(len(firstnames)):
        firstnames[i] = firstnames[i].strip("\n")
       
    with io.open("res/familynames.txt", mode = "r", encoding = "utf-8") as file:
        global lastnames
        lastnames = file.readlines()
    for i in range(len(lastnames)):
        lastnames[i] = lastnames[i].strip("\n")


def makeRecruit():
    rec = merc.Merc()
    random.seed()
    rec.firstname = random.choice(firstnames)
    rec.lastname = random.choice(lastnames)
    rec.pay = random.randint(2, 16)
    rec.strength = random.randint(1, 255)
    rec.dexterity = random.randint(1, 255)
    rec.intelligence = random.randint(1, 255)
    rec.charisma = random.randint(1, 255)
    rec.confidence = random.randint(1, 255)
    rec.birthday = events.Event.current - timedelta(days =365 * bellAge() + random.randint(1, 365))
    # Perks:
    for i in range(3): # max 3 perks
        prob = random.randint(0, 11) # probability
        if i >= prob:
            while True: # no duplicates
                perk = getRandomPerk()
                found = False
                for p in rec.perks:
                    if p.name == perk.name:
                        found = True
                if found: continue
                rec.perks.append(perk)
                break
    return rec


def make10Mercs():
    mercs = []
    for i in range(10):
        mercs.append(makeRecruit())
    return mercs


def make100Recruits():
    return list(map(lambda x:makeRecruit(), range(100)))


def getRandomPerk():
    rand = random.randint(0, len(merc.perkList) -1)
    return merc.perkList[rand]


def getRandomTroopType():
    rand = random.randint(0, 2)
    if rand == 0: return merc.UnitType.pikeman
    if rand == 1: return merc.UnitType.cavalry
    if rand == 2: return merc.UnitType.musketeer


def getRandomPikemen(count):
    pm = []
    for i in count:
       rec = makeRecruit()
       rec.xp.typ = merc.UnitType.pikeman
       pm.append(rec)
    return pm
    

def randomArmy(noofSectors, noofTroops):
    army = arm.Army(noofSectors)
    mercs = []
    for t in range(noofTroops):
        recruit = makeRecruit()
        recruit.xp.typ = getRandomTroopType()
        mercs.append(recruit)
    for i,s in enumerate(army.sectors):
        s.mercs = mercs[i:math.floor(len(mercs) /len(army.sectors)) *(i +1)]
    return army
