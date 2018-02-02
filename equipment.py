#equipment
from rogueIO import *
#the stats benefits from equipment. This needs to be expanded eventually
class equipStats:
	def __init__(self,power=0,modifier=0,defense=0,dice=1):
		self.power=power
		self.defense=defense
		self.modifier=modifier
		self.dice=1
	
	#Used to return a player to base once equipment is taken off
	def getPlayerStats(self,player):
		self.power=player.fighter.basePower
		self.modifier=player.fighter.powerModifier
		self.defense=player.fighter.defense
		self.dice=player.fighter.powerDice
	
	#used to update a player's stats once equipment is worn
	def setPlayerStats(self,player):
		player.fighter.power = self.power
		player.fighter.powerModifier=self.modifier
		player.fighter.defense=self.defense
		player.fighter.powerDice=self.dice
	
#This prevents players from equipping 10 weapons, say
class equipment:
	def __init__(self,weapon):
		self.weapon=weapon
		
class weapon:
	def __init__(self,weaponObject,numDice,newStats,type=None,oldStats=None):
		weaponObject.item.use_function=self.equip
		self.weaponObject=weaponObject
		self.weaponObject.item.equippable=True
		self.newStats=newStats
		self.oldStats=oldStats
		self.numDice=numDice
		self.type=type #the type is used to determine your skill bonus
	
	def equip(self,player,game_msgs):
		messagePrinter('You equip the ' + self.weaponObject.name,game_msgs)
		self.oldStats=equipStats()
		self.oldStats.getPlayerStats(player)
		self.newStats.setPlayerStats(player)
		messagePrinter('Player attack: ' + str(player.fighter.power),game_msgs)
		self.weaponObject.item.use_function=self.unequip #toggle
	
	def unequip(self,player,game_msgs):
		self.oldStats.setPlayerStats(player)
		self.weaponObject.item.use_function=self.equip
		messagePrinter('You unequip the ' + self.weaponObject.name,game_msgs)
		messagePrinter('Player attack: ' + str(player.fighter.power),game_msgs)
		
