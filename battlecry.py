#Battlecry logic
from rogueIO import *
import libtcodpy as libtcod

#this stops the battlecry and resets the player to base stats
def stopBattlecry(player,game_msgs):
	#temporary for you, not monsters - reset anything that could be modified by this
	player.fighter.power -= 1 
	player.fighter.defense = player.fighter.baseDefense
	player.fighter.battlecry = 0 #stop crying
	messagePrinter('You stop shouting your battlecry',game_msgs)

#This starts the battlecry and causes the effect to the player
def startBattlecry(player,game_msgs):
	#begin modifications.  This is very basic right now
	player.fighter.power += 1 
	player.fighter.battlecry = 1 #start crying
	messagePrinter('You start shouting your battlecry',game_msgs)

#Here we do the battlecry admin - subtract Voice, kill the cry if the player is out, and 
#increase Voice if the player is not chanting
def resolveBattlecry(player,game_msgs):
    if player.fighter.battlecry==1 and player.fighter.voice > 0:
		player.fighter.voice -= 2
		#player.fighter.power = player.fighter.basePower + 1
    elif player.fighter.battlecry == 1 and player.fighter.voice <= 0:
		messagePrinter('Your voice is too weak to continue your battlecry',game_msgs)
		stopBattlecry(player,game_msgs)
    if player.fighter.battlecry==0:
		if player.fighter.voice < player.fighter.maxVoice:
			player.fighter.voice += 1
		#player.fighter.power=player.fighter.basePower

#here we resolve the efffect of the battlecry on the enemy.  This involves considering
#the player's Name as well as the enemy type.  The battlecry will effect only those enemies that
#the player has directly targeted, but they will be permanent effects
def battlecryEffect(player,game_msgs,target):
	target.fighter.defense = target.fighter.baseDefense - 1 #the base case
	
	#now handle the case of an upgraded Name
	for c in  player.fighter.conquests:
		if c.number >= BASIC_CONQUEST and target.name == c.name:
			target.fighter.defense = target.fighter.baseDefense - 1 #the base case
	
	return target.fighter