#The questing subsystem
from rogueIO import *
import libtcodpy as libtcod
from menus import *	

class quest:
	def __init__(self,questList=None):
		self.questList=[]
		self.completed=False
		self.benefits=None
		
	def addQuest(self,sq):
		self.questList.append(sq)
		if self.benefits is None:
			self.benefits=sq.benefits
		else:
			self.benefits.mergeBenefits(sq.benefits)
	
	#This can be made much more swanky
	def isComplete(self,data):
		self.completed = True
		for sq in self.questList:
			if sq.isComplete(data) == False:
				self.completed=False
		

class subQuest:
	def __init__(self,benefits,winType):
		self.benefits=benefits #another class
		self.winType=winType #another class
	
	#data will be a list compiled by the quest system in the main game that depents on the individual quest 
	def isComplete(self,data):
		return self.winType.isComplete(data)

#Utility
class questBenefits:
	#perhaps getting a potion here?
	def __init__(self,Voice,Name):
		self.Voice=Voice
		self.Name=Name
	
	#TODO: MAKE THIS WAY BETTER
	def giveBenefits(self,player):
		player.fighter.maxVoice+=self.Voice
	
	def mergeBenefits(self,other):
		self.Voice += other.Voice
		self.Name += ', ' + other.Name #this will make weird names
		
# Quest types		
class reachLocationQuest:
	def __init__(self,data,x=None,y=None):
		if x is not None:
			self.x = x
			self.y = y
			data[MAP_INX][x][y].specialColor = libtcod.red
		else:
			self.randomizeLocation(data)
		
	def isComplete(self,data):
		
		#in this cast, "data" contains only the player object
		if data[PLAYER_INX].x == self.x and data[PLAYER_INX].y == self.y:
			return True
		return False
	
	def randomizeLocation(self,data):
		map=data[MAP_INX]
		portalPlaced = False
		portalX = 0
		portalY = 0
		lastRoomx = 0
		lastRoomy = 0
		for y in range(MAP_HEIGHT):
				for x in range(MAP_WIDTH):
					inRoom = map[x][y].isInRoom
					if inRoom == True and portalPlaced == False: #this is a location we can reach
						lastRoomx = x
						lastRoomy = y #ensures we place it somewhere
						w = libtcod.random_get_int(0, 0, 100)
						if w > 90:
							portalX = x
							portalY = y
							portalPlaced = True
							self.x=portalX
							self.y=portalY
							map[x][y].specialColor = libtcod.red
								
		if portalPlaced == False: #means we didn't place it at all
			portalX = lastRoomx
			portalY = lastRoomy
			self.x=portalX
			self.y=portalY
			map[x][y].specialColor = libtcod.red

class obtainItemQuest():
	def __init__(self,item,data,x=None,y=None): #item must be created first
		self.item=item
		if x is not None:
			self.x=x
			self.y=y #where to place the item
			data[OBJECTS_INX].append(item) #place it
		else:
			self.randomizeItemLocation(data)
	
	def randomizeItemLocation(self,data):
		lastRoomx = 0
		lastRoomy = 0
		itemPlaced = False
		for y in range(MAP_HEIGHT):
				for x in range(MAP_WIDTH):
					inRoom = data[MAP_INX][x][y].isInRoom
					if inRoom == True and itemPlaced == False: #this is a location we can reach
						lastRoomx = x
						lastRoomy = y #ensures we place it somewhere
						w = libtcod.random_get_int(0, 0, 100)
						if w > 90:
							self.item.x = x
							self.item.y = y
							data[OBJECTS_INX].append(self.item)
							itemPlaced=True
		if itemPlaced == False: #means we didn't place it at all
			self.item.x = lastRoomx
			self.item.y = lastRoomy
			data[OBJECTS_INX].append(self.item)
		
	#data needs to contain the inventory object
	def isComplete(self,data):
		if isItemInInventory(data[INVENTORY_INX],self.item.name):
			return True
		return False
	