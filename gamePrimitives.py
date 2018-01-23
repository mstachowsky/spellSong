#Contains basics that are needed to make the game work,
#like rectangles and tiles
class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None,specialColor=None):
        self.blocked = blocked
		
		#special_color lets us change the color of tiles if they are, say, doors etc.  Otherwise, the render function defaults to whatever it is
        self.specialColor = specialColor
        #all tiles start unexplored
        self.explored = False
 
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
		
		#whether a tile is in a room or a hallway is relevant to quests
        self.isInRoom = False
 
class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
 
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
 
    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
