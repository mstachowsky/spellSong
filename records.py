#Player records
from gameConsts import *


class conquest:
#a tile of the map and its properties
	def __init__(self, name):
		self.name=name
		self.number=1 #creating a new conquest means it is the first enemy of that type you've slain

#when the player kills an enemy target, update his conquest list
def updateConquest(player,name):
	#first, search the list for the name, if it's there
	found = 0
	for c in player.fighter.conquests:
		if c.name==name:
			c.number +=1
			found = 1
			#now update the player's Name.
			#TODO: this really should be better than just string search, to be honest
			if c.number >= BASIC_CONQUEST:
				if ' Slayer of ' not in player.trueName: #first conquest
					player.trueName += ', Slayer of ' + c.name + 's'
				elif c.name not in player.trueName:
					player.trueName += ',' + c.name + 's'
	if found==0:
		c = conquest(name)
		player.fighter.conquests.append(c)
	