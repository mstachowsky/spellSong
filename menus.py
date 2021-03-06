#This is going to hold all of the menus, like spell building etc

from gameConsts import *
import libtcodpy as libtcod #honestly just for random
from rogueIO import *

def menu(header, options, width):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
 
    #calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height
 
    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
 
    #print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
 
    #print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1
 
    #blit the contents of "window" to the root console
    x = SCREEN_WIDTH/2 - width/2
    y = SCREEN_HEIGHT/2 - height/2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
 
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    #convert the ASCII code to an index; if it corresponds to an option, return it
    index = key.c - ord('a')
    if index >= 0 and index < len(options): return index
    return None

	 
def msgbox(text, width=50):
    menu(text, [], width)  #use menu() as a sort of "message box"

#Currently doesn't allow for deleting words...
def spell_building_menu(header,dictionary):
	#show a menu with each item of the inventory as an option
    if len(dictionary) == 0:
        options = ['You don\'t know any Spell Words']
    else:
		options = []
		for wrd in dictionary:
			options.append(wrd)
		options.append('done')
    spellList = []
    index = menu(header, options, INVENTORY_WIDTH)
    newStr = options[index]
    oldHeader=header
    while(options[index] != 'done'):
		header=oldHeader + 'The spell currently is: \n'
		header += newStr
		spellList.append(options[index])
		index = menu(header, options, INVENTORY_WIDTH)
		newStr += options[index]
		
    if spellList: #if it isn't empty
		return spellList
    return None
	
def spell_menu(header,spells):
    #show a menu with each item of the inventory as an option
    if len(spells) == 0:
        options = ['You don\'t know any spells']
    else:
		options = []
		for spl in spells:
			options.append(spl.name + ', cost: ' + str(spl.cost))
 
    index = menu(header, options, INVENTORY_WIDTH)
 
    #if an item was chosen, return it
    if index is None or len(spells) == 0: return -1
    return index
	
def inventory_menu(header,inventory):
    #show a menu with each item of the inventory as an option
    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory]
 
    index = menu(header, options, INVENTORY_WIDTH)
 
    #if an item was chosen, return it
    if index is None or len(inventory) == 0: return None
    return inventory[index].item
	
def isItemInInventory(inventory, itemName):
	for item in inventory:
		if itemName == item.name:
			return True
	return False