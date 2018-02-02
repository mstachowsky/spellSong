from rogueIO import *
from battlecry import *
from records import *
from targetting import *
from gameConsts import *
import libtcodpy as libtcod
from random import *

class Fighter:
	#combat-related properties and methods (monster, player, NPC).
	def __init__(self, hp, defense, power, powerDice, voice=0,death_function=None, battlecry=0, powerModifier=0):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.baseDefense=defense #used when chanting
		self.power = power
		self.basePower=power #used when chanting
		self.powerDice=powerDice
		self.powerModifier=powerModifier #(like, +1 etc.  Will be useful when we equip weapons)
		self.death_function = death_function
		self.voice=voice #mana, basically
		self.maxVoice=10 #at  the moment, a default
		self.battlecry=battlecry
		self.conquests=[] #the array of conquests
		self.spellBook=[] #the "book of spells" (a list of spells...)
		self.casting=-1 #this variable is used to determine which spell is currently being cast.  It goes back to -1 when nothing is being cast, and is otherwise the index of the spell being cast in the spellbook
		self.dictionary=[] #the dictionary of words that the player knows
 
	def attack(self, target,game_msgs):
		#attack damage - compute the sum of all of the random dice rolls
		attackPower=0
		for i in range(0,self.powerDice):
			attackPower += randint(0,self.power)
		attackPower += self.powerModifier
		damage = attackPower - target.fighter.defense
 
		if damage > 0:
			#make the target take some damage
			messagePrinter(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.',game_msgs)
			target.fighter.take_damage(damage)
		else:
			messagePrinter(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!',game_msgs)
 
	def take_damage(self, damage):
		#apply damage if possible
		if damage > 0:
			self.hp -= damage
 
			#check for death. if there's a death function, call it
			oldSelf = self
			if self.hp <= 0:
				function = self.death_function
				if function is not None:
					function(self.owner)
 
	def heal(self, amount):
		#heal by the given amount, without going over the maximum
		self.hp += amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp


def player_move_or_attack(dx, dy, player,fov_map,context):
	
	#global fov_recompute
	fov_recompute=False
	#resolve any battlecry/chanting - this resolves it for the player
	
	resolveBattlecry(player,game_msgs)
	#the coordinates the player is moving to/attacking
	x = player.x + dx
	y = player.y + dy
	
	#try to find an attackable object there
	target = None
	for object in objects:
		if object.fighter and object.x == x and object.y == y:
			target = object
			break
	
#if we are casting, do it now
	if player.fighter.casting != -1:
		targetList=monsters_in_range(BASE_CAST_RANGE,player,fov_map)
		messagePrinter('Casting!',game_msgs)
		player.fighter.spellBook[player.fighter.casting].cast(player,targetList,game_msgs,context)
			
	#attack if target found, move otherwise
	if target is not None:
		name = target.name #to be used for conquests
		#resolve the cry
		if player.fighter.battlecry == 1:
			target.fighter = battlecryEffect(player,game_msgs,target)
		player.fighter.attack(target,game_msgs)
		
		#resolve conquest
		if target.fighter is None:
			updateConquest(player,name)
			messagePrinter(player.trueName,game_msgs)
		
	else:
		player.move(dx, dy)
		fov_recompute = True
	
	return fov_recompute	

	
class BasicMonster:
	#AI for a basic monster.
	def take_turn(self,fov_map,player):
		#a basic monster takes its turn. if you can see it, it can see you
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
 
			#move towards player if far away
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y)
 
			#close enough, attack! (if the player is still alive.)
			elif player.fighter.hp > 0:
				monster.fighter.attack(player,game_msgs)
 
class ConfusedMonster:
	#AI for a temporarily confused monster (reverts to previous AI after a while).
	def __init__(self, old_ai, num_turns=CONFUSE_NUM_TURNS):
		self.old_ai = old_ai
		self.num_turns = num_turns
 
	def take_turn(self):
		if self.num_turns > 0:  #still confused...
			#move in a random direction, and decrease the number of turns confused
			self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
			self.num_turns -= 1
 
		else:  #restore the previous AI (this one will be deleted because it's not referenced anymore)
			self.owner.ai = self.old_ai
			message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)
 