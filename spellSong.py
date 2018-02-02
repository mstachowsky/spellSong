import libtcodpy as libtcod
import math
import textwrap
import shelve

#my own libraries
from rogueIO import *
from gameConsts import *
from battlecry import *
from records import *
from spells import *
from menus import *
from objectDefs import *
from gamePrimitives import *
from renderUtilities import *
from targetting import *
from quests import *
from equipment import *
 
class Object:
	#this is a generic object: the player, a monster, an item, the stairs...
	#it's always represented by a character on screen.
	def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None, item=None):
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.trueName = name #this is used for various magicks
		self.color = color
		self.blocks = blocks
		self.fighter = fighter
		if self.fighter:  #let the fighter component know who owns it
			self.fighter.owner = self
 
		self.ai = ai
		if self.ai:  #let the AI component know who owns it
			self.ai.owner = self
 
		self.item = item
		if self.item:  #let the Item component know who owns it
			self.item.owner = self
 
	def move(self, dx, dy):
		#move by the given amount, if the destination is not blocked
		if not is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy
 
	def move_towards(self, target_x, target_y):
		#vector from this object to the target, and distance
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)
 
		#normalize it to length 1 (preserving direction), then round it and
		#convert to integer so the movement is restricted to the map grid
		dx = int(round(dx / distance))
		dy = int(round(dy / distance))
		self.move(dx, dy)
 
	def distance_to(self, other):
		#return the distance to another object
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)
 
	def distance(self, x, y):
		#return the distance to some coordinates
		return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
 
	def send_to_back(self):
		#make this object be drawn first, so all others appear above it if they're in the same tile.
		global objects
		objects.remove(self)
		objects.insert(0, self)
 
	def draw(self):
		#only show if it's visible to the player
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			#set the color and then draw the character that represents this object at its position
			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
 
	def clear(self):
		#erase the character that represents this object
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def handle_keys(key,objects,player,inventory,game_state):
	global fov_recompute
	
	ctx=[key,mouse,map,player,objects,fov_recompute,fov_map]
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt+Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
	elif key.vk == libtcod.KEY_ESCAPE:
		return 'exit'  #exit game
 
	if game_state == 'playing':
		#movement keys
		if key.vk == libtcod.KEY_UP:
			fov_recompute = player_move_or_attack(0, -1, player,fov_map,ctx)
 
		elif key.vk == libtcod.KEY_DOWN:
			fov_recompute = player_move_or_attack(0, 1, player,fov_map,ctx)
 
		elif key.vk == libtcod.KEY_LEFT:
			fov_recompute = player_move_or_attack(-1, 0, player,fov_map,ctx)
 
		elif key.vk == libtcod.KEY_RIGHT:
			fov_recompute = player_move_or_attack(1, 0, player,fov_map,ctx)
		elif key.vk != libtcod.KEY_CHAR:
			key_char = chr(key.c)
			return 'didnt-take-turn'
		elif key.vk == libtcod.KEY_CHAR:
			#test for other keys
			key_char = chr(key.c)
			otherKey=libtcod.Key()
			if key_char == 'g':
				#pick up an item
				for object in objects:  #look for an item in the player's tile
					if object.x == player.x and object.y == player.y and object.item:
						object.item.pick_up()
						break
				return 'took_turn'
 
			if key_char == 'i':
				#show the inventory; if an item is selected, use it
				chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n',inventory)
				if chosen_item is not None:
					chosen_item.use()
			#opening inventory does not count as a turn
			
			if key_char == 'd':
				#show the inventory; if an item is selected, drop it
				chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
				if chosen_item is not None:
					chosen_item.drop()
				return 'took_turn'
		
			if key_char == 'c': 
				if (player.fighter.battlecry==0 and player.fighter.voice>0): #battlecry
					startBattlecry(player,game_msgs)
				else:
					stopBattlecry(player,game_msgs)
		
			#cast a spell
			if key_char == 's':
				player.fighter.casting = -1 #SUPER SKETCH, NEED RE-DO!!
				targetList=monsters_in_range(BASE_CAST_RANGE,player,fov_map)
				message('Casting!')
				player.fighter.casting=spell_menu('Press the key next to an spell to cast it, or any other to cancel.\n',player.fighter.spellBook)
				if(player.fighter.casting != -1):
					player.fighter.spellBook[player.fighter.casting].cast(player,targetList,game_msgs,ctx)
					return 'took_turn'
			
			#forget a spell - this counts as a turn.  Anything to do with setting up magic counts as a turn
			if key_char == 'f':
				spellInx=spell_menu('Press the key next to an spell to delete it, or any other to cancel.\n',player.fighter.spellBook)
				if(spellInx != -1):
					del(player.fighter.spellBook[spellInx])
					return 'took_turn'

			if key_char == 'w': #write a spell
				spellList=spell_building_menu('Press the key next to a word to add it to the spell\n',player.fighter.dictionary)
				if spellList is not None:
					trySpell = spell()
					trySpell.buildFromWordList(spellList,bigList)
					#only add if it isn't already there
					isThere=False
					for sp in player.fighter.spellBook:
						if(sp.name == trySpell.name):
							isThere = True
					if not isThere:
						player.fighter.spellBook.append(trySpell)
				
			
			#be quiet (stop casting a continuous spell)
			if key_char == 'q':
				player.fighter.casting=-1
			#Stopping casting does not count as a turn
			return 'didnt-take-turn'
			
class Item:
	#an item that can be picked up and used.
	def __init__(self, use_function=None,equippable=False):
		self.use_function = use_function
		self.equippable=equippable
 
	def pick_up(self):
		#add to the player's inventory and remove from the map
		if len(inventory) >= 26:
			message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
		else:
			inventory.append(self.owner)
			objects.remove(self.owner)
			message('You picked up a ' + self.owner.name + '!', libtcod.green)
 
	def drop(self):
		#add to the map and remove from the player's inventory. also, place it at the player's coordinates
		objects.append(self.owner)
		inventory.remove(self.owner)
		self.owner.x = player.x
		self.owner.y = player.y
		message('You dropped a ' + self.owner.name + '.', libtcod.yellow)
 
	def use(self):
		#just call the "use_function" if it is defined
		if self.use_function is None:
			message('The ' + self.owner.name + ' cannot be used.')
		else:
			if self.equippable==False:
				if self.use_function() != 'cancelled':
					inventory.remove(self.owner)  #destroy after use, unless it was cancelled for some reason
			else:
				self.use_function(player,game_msgs) #we are equipping it
 
def is_blocked(x, y):
	#first test the map tile
	if map[x][y].blocked:
		return True
 
	#now check for any blocking objects
	for object in objects:
		if object.blocks and object.x == x and object.y == y:
			return True
 
	return False
 
def create_room(room):
	global map
	#go through the tiles in the rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			map[x][y].blocked = False
			map[x][y].block_sight = False
			map[x][y].isInRoom = True #tiles in rooms are in rooms
 
def create_h_tunnel(x1, x2, y):
	global map
	#horizontal tunnel. min() and max() are used in case x1>x2
	for x in range(min(x1, x2), max(x1, x2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
		
def create_v_tunnel(y1, y2, x):
	global map
	#vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
 
def make_map():
	global map
 
	#the list of objects with just the player
	objects.append(player)
 
	#fill map with "blocked" tiles
	map = [[ Tile(True)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]
 
	rooms = []
	num_rooms = 0
 
	for r in range(MAX_ROOMS):
		#random width and height
		w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#random position without going out of the boundaries of the map
		x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
		y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
 
		#"Rect" class makes rectangles easier to work with
		new_room = Rect(x, y, w, h)
 
		#run through the other rooms and see if they intersect with this one
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
 
		if not failed:
			#this means there are no intersections, so this room is valid
 
			#"paint" it to the map's tiles
			create_room(new_room)
 
			#center coordinates of new room, will be useful later
			(new_x, new_y) = new_room.center()
 
			if num_rooms == 0:
				#this is the first room, where the player starts at
				player.x = new_x
				player.y = new_y
			else:
				#all rooms after the first:
				#connect it to the previous room with a tunnel
 
				#center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms-1].center()
 
				#draw a coin (random number that is either 0 or 1)
				if libtcod.random_get_int(0, 0, 1) == 1:
					#first move horizontally, then vertically
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					#first move vertically, then horizontally
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)
 
			#add some contents to this room, such as monsters
			place_objects(new_room)
 
			#finally, append the new room to the list
			rooms.append(new_room)
			num_rooms += 1
 
 
def place_objects(room):
	#choose random number of monsters
	num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)
 
	for i in range(num_monsters):
		#choose random spot for this monster
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
 
		#only place it if the tile is not blocked
		if not is_blocked(x, y):
			if libtcod.random_get_int(0, 0, 100) < 80:  #80% chance of getting an orc
				#create an orc
				fighter_component = Fighter(hp=10, defense=0, power=3, powerDice = 1, death_function=monster_death)
				ai_component = BasicMonster()
 
				monster = Object(x, y, 'o', 'orc', libtcod.desaturated_green,
					blocks=True, fighter=fighter_component, ai=ai_component)
			else:
				#create a troll
				fighter_component = Fighter(hp=16, defense=1, power=4, powerDice=1, death_function=monster_death)
				ai_component = BasicMonster()
 
				monster = Object(x, y, 'T', 'troll', libtcod.darker_green,
					blocks=True, fighter=fighter_component, ai=ai_component)
 
			objects.append(monster)
 
	#choose random number of items
	num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)
	
	for i in range(num_items):
		#choose random spot for this item
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
 
		#only place it if the tile is not blocked
		if not is_blocked(x, y):
			dice = libtcod.random_get_int(0, 0, 100)	
			if dice < 70:
				#create a healing potion (70% chance)
				item_component = Item(use_function=cast_heal)
 
				item = Object(x, y, '!', 'healing potion', libtcod.violet, item=item_component)
			elif dice < 70+10:
				#create a lightning bolt scroll (10% chance)
				item_component = Item(use_function=cast_lightning)
 
				item = Object(x, y, '#', 'scroll of lightning bolt', libtcod.light_yellow, item=item_component)
			elif dice < 70+10+10:
				#create a fireball scroll (10% chance)
				item_component = Item(use_function=cast_fireball)
 
				item = Object(x, y, '#', 'scroll of fireball', libtcod.light_yellow, item=item_component)
			else:
				#create a confuse scroll (10% chance)
				item_component = Item(use_function=cast_confuse)
 
				item = Object(x, y, '#', 'scroll of confusion', libtcod.light_yellow, item=item_component)
	 
			objects.append(item)
			item.send_to_back()  #items appear below other objects

def message(new_msg, color = libtcod.white):
		messagePrinter(new_msg,game_msgs,color)
 

 
def player_death(player):
	#the game ended!
	global game_state
	message('You died!', libtcod.red)
	game_state = 'dead'
 
	#for added effect, transform the player into a corpse!
	player.char = '%'
	player.color = libtcod.dark_red
 
def monster_death(monster):
	#transform it into a nasty corpse! it doesn't block, can't be
	#attacked and doesn't move
	message(monster.name.capitalize() + ' is dead!', libtcod.orange)
	monster.char = '%'
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'remains of ' + monster.name
	monster.send_to_back()
 
 
def cast_heal():
	#heal the player
	if player.fighter.hp == player.fighter.max_hp:
		message('You are already at full health.', libtcod.red)
		return 'cancelled'
 
	message('Your wounds start to feel better!', libtcod.light_violet)
	player.fighter.heal(HEAL_AMOUNT)
 
def cast_lightning():
	#find closest enemy (inside a maximum range) and damage it
	monster = closest_monster(LIGHTNING_RANGE, player, fov_map)
	if monster is None:  #no enemy found within maximum range
		message('No enemy is close enough to strike.', libtcod.red)
		return 'cancelled'
 
	#zap it!
	message('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is '
		+ str(LIGHTNING_DAMAGE) + ' hit points.', libtcod.light_blue)
	monster.fighter.take_damage(LIGHTNING_DAMAGE)
 
def cast_fireball():
	#ask the player for a target tile to throw a fireball at
	message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan)
	(x, y) = target_tile(key,mouse,map,player,objects,fov_recompute,fov_map)
	if x is None: return 'cancelled'
	message('The fireball explodes, burning everything within ' + str(FIREBALL_RADIUS) + ' tiles!', libtcod.orange)
 
	for obj in objects:  #damage every fighter in range, including the player
		if obj.distance(x, y) <= FIREBALL_RADIUS and obj.fighter:
			message('The ' + obj.name + ' gets burned for ' + str(FIREBALL_DAMAGE) + ' hit points.', libtcod.orange)
			obj.fighter.take_damage(FIREBALL_DAMAGE)
 
def cast_confuse():
	#ask the player for a target to confuse
	message('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)
	monster = target_monster(key,mouse,map,player,objects,fov_recompute,fov_map,CONFUSE_RANGE)
	if monster is None: return 'cancelled'
 
	#replace the monster's AI with a "confused" one; after some turns it will restore the old AI
	old_ai = monster.ai
	monster.ai = ConfusedMonster(old_ai)
	monster.ai.owner = monster  #tell the new component who owns it
	message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', libtcod.light_green)
 
def save_game():
	#open a new empty shelve (possibly overwriting an old one) to write the game data
	file = shelve.open('savegame', 'n')
	file['map'] = map
	file['objects'] = objects
	file['player_index'] = objects.index(player)  #index of player in objects list
	file['inventory'] = inventory
	file['game_msgs'] = game_msgs
	file['game_state'] = game_state
	file.close()
 
def load_game():
	#open the previously saved shelve and load the game data
	global map, objects, player, inventory, game_msgs, game_state
 
	file = shelve.open('savegame', 'r')
	map = file['map']
	objects = file['objects']
	player = objects[file['player_index']]  #get index of player in objects list and access it
	inventory = file['inventory']
	game_msgs = file['game_msgs']
	game_state = file['game_state']
	file.close()
 
	initialize_fov()
 
def new_game():
	global player, inventory, game_msgs, game_state
 
	#create object representing the player
	fighter_component = Fighter(hp=30, defense=2, power=PLAYER_DAMAGE_BASE, powerDice=1, voice=10, death_function=player_death)
	player = Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component)
	
	#INIT PLAYER SPELLBOOK - THIS IS THE EASY WAY, MUST BE CHANGED LATER
	player.fighter.spellBook = []#spellList
		
	#generate map (at this point it's not drawn to the screen)
	make_map()

	initialize_fov()
 
	game_state = 'playing'
	inventory = []
 
	#a warm welcoming message!
	message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)
 
def initialize_fov():
	global fov_recompute, fov_map
	
	fov_recompute=True
	fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
	
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
 
	libtcod.console_clear(con)  #unexplored areas start black (which is the default background color)
 
#This function will rock the quest system
def play_game():
	global key, mouse
 
	player_action = None
 
	mouse = libtcod.Mouse()
	key = libtcod.Key()
	
	questList=[]

	#Make me a new quest.  Very clearly not how we're going to do this for real
	newWords=['troll']
	benefits=questBenefits(1,'Non',newWords)
	qData = [player, map, objects, inventory,game_msgs] 
	locQuest=reachLocationQuest(qData)
	#locQuest.randomizeLocation(qData)
	#This first quest is a "find the ring and escape" quest, hard-coded.  So we need to randomly place the escape and the ring
	item_component = Item()
 
	item = Object(player.x+1, player.y, '*', 'Ring', libtcod.violet, item=item_component)
	itQuest=obtainItemQuest(item,qData)
	#itQuest.randomizeItemLocation(qData)
	
	quest1=subQuest(benefits,locQuest)
	quest2=subQuest(benefits,itQuest)
	
	mainQuest=quest()
	mainQuest.addQuest(quest1)
	mainQuest.addQuest(quest2)
	questList.append(mainQuest)
	
	#make the player's dictionary for testing
	player.fighter.dictionary = ['strong','banish','orc']

	#make up some weapons - there are only so many weapons, so they are all global constants.  This will be moved away once we get Item moved
	daggerStats=equipStats(8,0,0)
	daggerItem_component = Item()
	daggerItem = Object(player.x+2, player.y, ')', 'Dagger', libtcod.violet, item=daggerItem_component)
	dagger=weapon(daggerItem,1,daggerStats)
		
	inventory.append(dagger.weaponObject)
	
	while not libtcod.console_is_window_closed():
		#render the screen
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
		render_all(mouse,map,player,objects,fov_recompute,fov_map)
 
		libtcod.console_flush()
 
		#erase all objects at their old locations, before they move
		for object in objects:
			object.clear()
 
		#handle keys and exit game if needed
		player_action = handle_keys(key,objects,player,inventory,game_state)
		if player_action == 'exit':
		   # save_game()
			break
		qData = [player, map, objects, inventory,game_msgs] #upate the quest data
		
		#Once the player takes an action, check quests
		for qu in questList:	
			qu.isComplete(qData)
			if qu.completed == True: 
				qu.benefits.giveBenefits(player)
				inx = questList.index(qu)
				del(questList[inx])
		
		#let monsters take their turn
		if game_state == 'playing' and player_action != 'didnt-take-turn':
			for object in objects:
				if object.ai:
					object.ai.take_turn(fov_map,player)
 
def main_menu():
	img = libtcod.image_load('menu_background.png')
 
	while not libtcod.console_is_window_closed():
		#show the background image, at twice the regular console resolution
		libtcod.image_blit_2x(img, 0, 0, 0)
 
		#show the game's title, and some credits!
		libtcod.console_set_default_foreground(0, libtcod.light_yellow)
		libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER,
			'Spell Song')
		libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT-4, libtcod.BKGND_NONE, libtcod.CENTER,
			'Underlying game logic from the libtcod python tutorial By Jotaf')
		libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER,
			'Story and game mechanics by Mike Cooper-Stachowsky')
		#show options and wait for the player's choice
		choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)
 
		if choice == 0:  #new game
			new_game()
			play_game()
		if choice == 1:  #load last game
			try:
				load_game()
			except:
				msgbox('\n No saved game to load.\n', 24)
				continue
			play_game()
		elif choice == 2:  #quit
			break
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)

main_menu()

