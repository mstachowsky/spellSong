# spellSong

Based heavily off of the libtcodpy python tutorial by Jotaf.  The map generation, FOV computation, movement, orcs and trolls, and some of the basic items come from that tutorial [[http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod]]

Requires: Python 2.7

To make this run (I think): download to a new folder.  Make a new directory inside this new folder called "libtcodpy".  Put the files "__init__.py" and "cprotos.py" into the libtcodpy folder.  Run the "spellSong.py" script.

## Commands:

Arrow keys to move
- i - open inventory (then choose a letter)
- g - get item (move over an item, type g)
- c - Battlecry: start shouting your battlecry.  When the game starts, this gives you a +1 to attack and your target a -1 to defense.  hitting 'c' while shouting will stop the battlecry
- s - cast spells.  Open the spell menu and choose which spell.  Works like inventory
- q - be "quiet" - for spells that are active continuously, this turns them off
- w - write spells.  Opens the spell building menu.  Slightly buggy at this time
- esc - leave the game
- Mouse - context dependent.  Hovering mouse over something names it, mouse is also used to target some spell scrolls.

## How Battlecry currently works

As you slay more creatures of the same type, your Name grows to include "slayer of...".  For instance, kill 2 orcs and you are known as "slayer of Orcs".  This provides an additional -1 to an Orc's defense if you are shouting your cry.  Currently there are only orcs and trolls.

Battlecry uses Voice at a rate of 2 per turn.  You regenerate at a rate of 1 per turn if you are not shouting.

## How spells currently work

Spells are built from spell words that the player knows.  The player starts with a set of spell words, and can learn more through quests.  Spell words are broken into "noun" spells, that have an effect on a particular thing, "environment" spells, that have an effect on a particular aspect of the environment, and "modifier" spells that enhance particular spell effects.

### How "strong" works

The spellword strong is used to to increase the effect of a given spell.  It multiplies the potential effect of any spell by 2.  The effects are cumulative, so a spell with two "strong" words will multiply the effect by 2x2=4

### Building a noun spell

Noun spells confer debuffs to the enemy or enemies named in the spell.  There are two types of enemies, orcs and trolls, currently implemented.  Noun spells search for visible targets of the appropriate type and have a random chance to reduce that enemy's attack power or defense, and a random chance of success.

For instance, the spell "orc" will have a 30% chance of success and, if successful, a 50/50 chance of debuffing the attack or defense of the orc by 1 point.  The spell "strong orc" has a 30% chance of success, a 50/50 chance of either defense or attack being debuffed, but now by a factor of 2 (due to strong) x 1 (the base effect of a noun) = 2.

Noun spells require you to be chanting them continuously.  You stop chanting either by pressing "q" or by running out of Voice.  At the moment, noun spells do not return the targets' stats to their normal levels, but that will be implemented soon.

### Building an environment spell

There is currently only one environment spell implemented, "banish".  This requires you to click an enemy and click a location within your field of view to banish it to.  Base banish distance is 4 squares, and this gets multiplied as above by "strong".

### Cost of casting

The cost of casting any spell is given by cost = cost + pow(2,numWords-1), with cost initially being 0.  So if you cast a 1-word spell, it costs 0 + pow(2,0) = 1.  Casting a 4 word spell requires cost = 0 + pow(2,0) + pow(2,1) + pow(2,2) + pow(2,3) = 15 Voice.  The player currently has only 10 Voice, so you are stuck to 3 word spells.
