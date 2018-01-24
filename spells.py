#Spells
from gameConsts import *
from rogueIO import *
import libtcodpy as libtcod #honestly just for random
from targetting import *
#utility functions used by everything
def decreaseStat(target, spell): #used by stat decreasing spells
	x = libtcod.random_get_int(0,0,1)
	if x==1:
		return 'power'
	else:
		return 'defense'

#The class stores a useFunction, which is the function that is called when the spell is used
class spell:
	def __init__(self,useFunction=None):
		self.useFunction=useFunction #this is the ID of the eventual castable function after spell parsing
		self.name=''
		self.targetList=[] #a list of target names...for now. This needs some thought.
		self.cost=0
		self.chance=BASE_SPELL_CHANCE
		self.effectMultiplier=0
		self.numWords=0
		self.stat=''
		self.data=[] #a generic "data" list to allow for LOTS of generality. This is spell-dependent, and it updates every time a spell is *build*
		self.castingData=[] #this is the data that the spell is acting on (like the name of the enemy, for instance).  It is set once a spell is built
		
		#Basically, data itself is a scratchpad that gets modified for every word.  castingData might get over-written as the spell is being built, but it contains data that is used to determine the target etc. of the spell once it's cast, so it is relevant beyond the building stage
		
	def cast(self,player,targetList,game_msgs,context):
		if player.fighter.voice >= self.cost:
			self.useFunction(self,targetList,game_msgs,context)
			player.fighter.voice -= self.cost
		else:
			messagePrinter('Your voice is not strong enough to cast that spell',game_msgs)
			player.fighter.casting=-1 #stop casting
			
	#wordsInSpell = a list of strings, wordList = a list of spellWord objects
	def buildFromWordList(self,wordsInSpell,wordList):
		spellList = []
		for wrd in wordsInSpell:
			for spWord in wordList:
				if (wrd == spWord.word):
					spellList.append(spWord)
		buildSpell(spellList,self)
#This class is for individual words, that get put together into a spell word list (sentence...) to build a spell
#The updateFunction is what is called to update the spell object itself 
class spellWord:
	def __init__(self,word,updateFunction=None,castFunction=None):
		self.word = word
		self.updateFunction=updateFunction
		self.castFunction=castFunction
	
#the actual spell building function - this needs to be MUCH more complex!!
#wordList is a list of spellWords, spell is the spell we are buildings
def buildSpell(wordList,spell):
	for word in wordList:
		spell.name += word.word + ' '
		word.updateFunction(word,spell)

#Some individual word functions.  Words get at most 2 functions:  buildWord - adds the word to the spell, and castWord - the effect of casting
	
def buildNoun(word,spell): #should work for any generic Noun
	if word.word not in spell.targetList:
		spell.targetList.append(word.word)
	spell.cost = spell.cost + 2**spell.numWords
	#Must increase effect.  However, if we have several nouns, we don't want them to be cumulative, or else there's no point in using "strong"
	if spell.effectMultiplier == 0:
		spell.effectMultiplier = 1
	spell.numWords += 1
	if word.word not in spell.castingData:
		spell.castingData.append(word.word)
	if spell.useFunction==None:
		spell.useFunction=word.castFunction
		
#Casting functions.  Note: these always have to have the same arguments, so we need to be careful
#before defining too many spells about how this will work, let's do it generically.  Also note: this currently doesn't allow for buffs!
def castNoun(spell,targetList,game_msgs,context=None,player=None):
	#make sure that the target list is not empty
	if not targetList:
		return 'No targets'
	
	#loop through enemies within ear shot
	for target in targetList:
		
		#first, compute the success or failure
		success = libtcod.random_get_int(0, 0, 100)
		if target.name not in spell.castingData:
			return 'wrong target' #Basically do nothing if you're not attacking the right thing anyway
		if spell.chance < success:
			messagePrinter('Your chanting has no effect', game_msgs, color = libtcod.red)
		else:
			if spell.stat == '': #get a random stat
				spell.stat = decreaseStat(target,spell)
			#now actually decrease the stat
			if spell.stat == 'power':
				target.fighter.power = target.fighter.basePower - spell.effectMultiplier
			elif spell.stat == 'defense':
				target.fighter.defense = target.fighter.baseDefense - spell.effectMultiplier
			messagePrinter('The ' + target.name + '\'s ' + spell.stat + 'fell by ' + str(spell.effectMultiplier), game_msgs, color = libtcod.green)
		
#Strong has no use function,  just a build function
def buildStrong(word,spell):
	spell.cost = spell.cost + 2**spell.numWords
	#Must increase effect - this makes for an INSANELY powerful spell
	#if you chain them, so definitely some balance needed
	if spell.effectMultiplier != 0:
		spell.effectMultiplier *= STRONG_MULTIPLIER
	else:
		spell.effectMultiplier = 2 #this is the first word we see
	spell.numWords += 1
	
	
#Environment spells
def buildBanish(word,spell):
	if spell.effectMultiplier == 0:
		spell.effectMultiplier = 1
	spell.cost = spell.cost + 2**spell.numWords
	spell.numWords +=1
	spell.useFunction=word.castFunction

	
#Lots left to do here.  Need to also include some kind of tile coloring so that you can see where they can/cannot go.  This is a generic "click the range" spell, so having a "color range" funcctiln that colors the tiles within range will be a great boon for this library.	

##BIG WARNING: cannot cancel this spell.  Need to fix the when target is none thing
def castBanish(spell,targetList,game_msgs,context):
	messagePrinter('Left click to select your target',game_msgs)
	target = target_monster(context[0],context[1],context[2],context[3],context[4],context[5],context[6])
	
	maxDist = BANISH_MULTIPLIER*spell.effectMultiplier
	
	#here we should re-render the map so we can see where to put them
	
	
	messagePrinter('Left click to select the location to banish them to',game_msgs)
	messagePrinter('The spell can banish up to a maximum of ' + str(maxDist) + ' squares',game_msgs)
	context[3].fighter.casting=-1 #one-shot - always stop casting
	(x,y)=target_tile(context[0],context[1],context[2],context[3],context[4],context[5],context[6])
	
	if x is not None:
		dx = x-target.x
		dy = y-target.y
		
		if (target is not None) and (dx < maxDist) and (dy < maxDist):
			targetList.append(target)
			messagePrinter('Banishing: ' + target.name,game_msgs);
			
			if target.fighter.hp >0:
				target.move(x-target.x,y-target.y)
				libtcod.console_clear(con)
		else:
			messagePrinter('Target location is too far!',game_msgs)
			context[3].fighter.casting=-1
			return 'No target'
	else:
		return 'No target'