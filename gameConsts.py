import libtcodpy as libtcod #needed for some constant vars

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
 
#size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 43
 
#sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
INVENTORY_WIDTH = 50
 
#parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3
MAX_ROOM_ITEMS = 2
 
#scroll values
HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
CONFUSE_NUM_TURNS = 10
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12

#Spell values
BASE_SPELL_CHANCE = 100
STRONG_MULTIPLIER=2
BASE_CAST_RANGE = 10
BANISH_MULTIPLIER=4

#Quest data indices
PLAYER_INX = 0
MAP_INX=1
OBJECTS_INX=2
INVENTORY_INX=3
MSGS_INX=4

#level values
BASIC_CONQUEST = 2
 
FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True  #light walls or not
TORCH_RADIUS = 10
 
LIMIT_FPS = 20  #20 frames-per-second maximum

#Console stuff 
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)


#color constants
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50) 


# Useful globals (yes...I know...)
objects = []
    #create the list of game messages and their colors, starts empty
game_msgs = []

#An absurdly useful context class that will prevent me from using all of these globals eventually
class gameContext:
	def __init__(self,key,mouse,map,fov_map,fov_recompute,player=None,objects=None):
		self.key = key
		self.mouse=mouse
		self.map=map
		self.fov_map=fov_map
		self.fov_recompute=fov_recompute
		self.player=player;
		self.objects=objects
