from rogueIO import *
from battlecry import *
from records import *
from targetting import *
from gameConsts import *

class Fighter:
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power, voice=0, death_function=None, battlecry=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.baseDefense=defense #used when chanting
        self.power = power
        self.basePower=power #used when chanting
        self.death_function = death_function
        self.voice=voice #mana, basically
        self.maxVoice=10 #at  the moment, a default
        self.battlecry=battlecry
        self.conquests=[] #the array of conquests
        self.spellBook=[] #the "book of spells" (a list of spells...)
        self.casting=-1 #this variable is used to determine which spell is currently being cast.  It goes back to -1 when nothing is being cast, and is otherwise the index of the spell being cast in the spellbook
 
    def attack(self, target,game_msgs):
        #a simple formula for attack damage
        damage = self.power - target.fighter.defense
 
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
