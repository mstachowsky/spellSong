#Handles key presses during the game

from gameConsts import *
import libtcodpy as libtcod #honestly just for random

def handle_keys(key,objects,player,inventory,game_state):
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  #exit game
 
    if game_state == 'playing':
        #movement keys
        if key.vk == libtcod.KEY_UP:
            player_move_or_attack(0, -1)
 
        elif key.vk == libtcod.KEY_DOWN:
            player_move_or_attack(0, 1)
 
        elif key.vk == libtcod.KEY_LEFT:
            player_move_or_attack(-1, 0)
 
        elif key.vk == libtcod.KEY_RIGHT:
            player_move_or_attack(1, 0)
        else:
            #test for other keys
            key_char = chr(key.c)
            otherKey=libtcod.Key()
            if key_char == 'g':
                #pick up an item
                for object in objects:  #look for an item in the player's tile
                    if object.x == player.x and object.y == player.y and object.item:
                        object.item.pick_up()
                        break
 
            if key_char == 'i':
                #show the inventory; if an item is selected, use it
                chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n',inventory)
                if chosen_item is not None:
                    chosen_item.use()
 
            if key_char == 'd':
                #show the inventory; if an item is selected, drop it
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()
            
			#battlecry handling is a hack at the moment
            if key_char == 'x' and player.fighter.battlecry==1: #stop battlecry
				stopBattlecry(player,game_msgs)
				
            if key_char == 'c' and player.fighter.battlecry==0 and player.fighter.voice>0: #battlecry
				startBattlecry(player,game_msgs)
			
			#cast a spell
            if key_char == 's':
				player.fighter.casting = 0 #SUPER SKETCH, NEED RE-DO!!
			
			#be quiet (don't cast)
            if key_char == 'q':
				player.fighter.casting=-1
            return 'didnt-take-turn'