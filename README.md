# spellSong

Based heavily off of the libtcodpy python tutorial by Jotaf.  I take no credit for most of this game at the moment.

Requires: Python 2.7

To make this run (I think): download to a new folder.  Make a new directory inside this new folder called "libtcodpy".  Put the files "__init__.py" and "cprotos.py" into the libtcodpy folder.  Run the "spellSong.py" script.

## Commands:

Arrow keys to move
i - open inventory (then choose a letter)
g - get item (move over an item, type g)
c - Battlecry: start shouting your battlecry.  When the game starts, this gives you a +1 to attack and your target a -1 to defense
s - stop your battlecry
esc - leave the game
Mouse - context dependent.  Hovering mouse over something names it, mouse is also used to target some spell scrolls.

## How Battlecry currently works

As you slay more creatures of the same type, your Name grows to include "slayer of...".  For instance, kill 2 orcs and you are known as "slayer of Orcs".  This provides an additional -1 to an Orc's defense if you are shouting your cry.  Currently there are only orcs and trolls.

Battlecry uses Voice at a rate of 2 per turn.  You regenerate at a rate of 1 per turn if you are not shouting.
