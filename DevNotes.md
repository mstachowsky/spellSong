# Forever dev notes

## Quest types

The quests will need to be generated randomly.  Exactly how to communicate this to the player is unknown at the moment, but that is secondary.  From Roguebasin, here are a few types of quests that might be randomly generated:


THE ADVENTURER
- Reach a certain location
- Find n objects and bring them to a person or location
- Something strange is going on. Track the source and stop it
- Escape from the trap (dungeon)

THE WARRIOR
- Kill n monsters (of a certain type)
- Clear a location from monsters

COMPETING WITH THE ENEMY/ARCHENEMY
- Get an object from the archenemy
- Get an object from a location to defeat the archenemy
- Steal an object from the enemy

That basically sums up some fairly standard quest types.  Some other things that were suggested:

WORLD-INTERACTION
- Use words of power to put out fires/make plants grow
- Talk to someone and pursuade them to do something

### Getting quests

The player will eventually always start in the "town" area.  In that area will always be an NPC called the "Bulletin Bard", who has a short list of quests that are available at the beginning.

## Mechanics

### Magic

Magic is performed through words of power.  Words of power are from a language that has rules.  Speaking a single word is essentially the lowest level spell you can use.  Stringing words together may create spells or gibberish, and must be tested.  Thus the player gets access to a spell book that they write in.

Generally, the longer the spell the more Voice it takes to say it.  In fact, each word has a base Voice usage.  The Voice use for a spell is just the addition of all of the words.  Thus you can't make an omni-powerful god spell by stringing a bunch of strength words if you don't have the Voice to chant it.  Attempting to chant a spell that you don't have enough Voice for will still cast SOMETHING, so the order of your words is important.  You will chant until you run out of voice.

#### Single words and strings

Words come in a few flavours:

- Nouns - nouns give power over the thing named to varying degrees while the word is being chanted.  Chanting uses Voice, so you can't chant indefinitely.  
  - General nouns - knowing the general noun, like "enemy", is the weakest word but affects the most things.  For instance, just chanting "enemy" is a word of power that has the chance to randomly reduce a stat of all enemies within earshot.  That chance is lower than it would be if the specific enemy's name is known.
  - Specific nouns - knowing the exact name of thing increases the chances of a spell being effective on that thing, at the expense of no longer being general.  For instance, chanting "Dragon" will be a spell that dramatically increases the chances of reducing a stat of all dragons in earshot, but is totally useless on orcs.
  - Self - a very special word that you learn early.  Chanting your own name has a chance of increasing a stat.
- Stats - knowing the name of a stat you want to change greatly increases the chances of a spell being effective, but you also need a target.  You can't just chant "speed", as that would be meaningless.  You'd say "Dragon Speed", and that would cause the dragon's speed to decrease if successful.  It allows greater control over a noun chant by focusing on the stat you want to reduce, and also further increases the chances of success.  "Self speed", similarly, increases your own speed.  Stat spells last as long as you are chanting them, which uses Voice.
- Elementals - your basic offensive spells.  Knowing a word like "fire" casts a fire spell at a targeted enemy.  These require a targetting system, probably via mouse.  
  - Enhanced elementals with nouns - if you use a noun you enhance the effectiveness in the same way as all nouns.  "Fire enemy" is a +1 effect, for instance, while "fire dragon" would be +2 or something against only dragons.  "Fire self" casts a protective spell on you.
- Enhancement words - these are words that strengthen effects of other spells, but are otherwise useless on their own.  This lets you build spells.  Enhancement words can be stacked together, at the expense of more Voice.  So you can say "Strong Strong Strong Strong Fire Dragon" to make a +4 Fire with +2 against Dragons, but it requires 6x the voice of just casting Fire.
  - Ehancements that encapsulate - Rather than stringing together a billion "Strongs", you can eventually learn words like "Powerful" or something, which is like casting 2 Strongs.  The benefit is that the Voice required is lower, but by diminishing amounts.  For instance, if Strong takes 1 Voice, then 2 Strongs takes 2 Voice but Powerful only takes 1.5 or something like that.  Godly, the next after Powerful, might be 3xStrong but use 2.3 Voice or something.  The exact balance needs work of course.
- Imbue - a special word that modifies a spell to target an item and store itself there.  Any spell can be Imbued.  Items can store only so much Voice, though, and imbuing away from an Altar takes Voice from you, just like casting the spell, with the added cost of Imbue.  Once you imbue an item with one spell, it can only be imbued with that same spell until you run out of charges (or just use it until it's empty).  So you can't store a healing spell and a fireball in the same ring at the same time.
- God words - these are words that cannot be invoked by a human except at an Altar.  At an Altar, the player can invoke a spell directly, or imbue items.  Item names don't need to be learned (that would be absurd) but Imbue does.  Casting any spell at an Altar still requires Voice for each word, including the item name.  God words work otherwise just like normal spells, so they can be modified.  The target of a god word is always self - the gods confer only favours, never disadvantages.
  - Heal - Heal is a god word. There is no way to cast a healing spell except by imbuing an item.
  - Bless - increases all stats for a period of time
  - Shield - increases max hit points using a magic shield
  - Regenerate - a low-level heal that is active for a period of time, regenerating as you go
  - God names - each god is associated with a particular effect.  Once you learn their names, you can imbue an item with their name just like a regular spell.  Calling upon their favour from an item causes their effect.  Exactly which gods exist and what their effects are is an unknown at the moment, and will probably be randomly generated.

### Offensive vs. persuading spells
I'm still on the fence about whether we should allow offensive spells. For instance, if "fireball" is a good idea.  I am happy to have scrolls that do this, but I'm not so sure about words of power.   It would make magic more interesting if you could only affect stats/defend yourself.  However, I'd like to consider also the idea of basic, familiar magic.  Maybe we could think of some spells that are interesting, but not necessarily offensive.  For instance, "push" - move an enemy back, if there is empty space available, "collect" - draw an item into your inventory (basically not upgradeable, you either know it or you don't).  I like this idea.  No offense, just really useful magic.

Some interesting ones:

Block - blocks a tile (or set of tiles as it gets stronger), creating an impassable wall
Banish - randomly transports a monster at least 2 squares away from player, +modifiers
Reach - get an item into inventory (no modifiers, just do it)
Reveal - reveal an area on the map (size determined by modifiers)
Impress - impress a person (make them think your Name is bigger than it is.  Modifiers increase chances of success)

#### Language rules

A spell is made up of modifiers and actions.  Actions are always required, or else the spell does nothing.  Elementals and stats are always actions, never modifiers.  Nouns are actions if no other actions are in the spell.  So "Strong Dragon" casts the Dragon debuff spell with the strong modifier.  However, if there are actions in the spell the noun becomes a target modifier - Strong Dragon Fire targets the Dragon with strong fire.

#### Voice

I think a key theme to the game will be the power of words and sound.  As a player learns more power words, and strings together more Names/spells etc, they will get more benefit.   However, there are limits.  One of those limits will be their Voice.  It's essentially a mana system.  To speak a word of power, or to shout a battle cry, puts a strain on the voice more than just speaking.  In fact, we might decide to increase the strength of a word of power with a Voice modifier - spells that are shouted are more powerful than those that are whispered, but put greater strain on your voice.  Voice recovers over time, of course, and the more you use it the stronger you get.

#### Favours

All words of power are linked to a particular Being (probably just gods, but I'm hoping to have a mythology generator going eventually).  Using a word increases your favour with that Being and reduces it with any Beings that are in conflict.  For instance, if there is a god of life and a god of blood, they might be in conflict.  The healing word for the god of life might be a weak but continuous healing or regeneration, while the healing word for the god of blood might be to take health from enemies.  Using either one will reduce the effectiveness of the other.  Some things might be neutral as well.

### Names

As you go through quests, or slay enough enemies of a certain type, your character begins to craft his Name.  This is used for respect and for the battlecry.

There will only be so many Names available, and some Names are given either through actions or  through quests.  For instance, you gain the name Slayer of (monster name) by slaying, say, 10 of a particular type of monster, but you might also be given that Name by slaying a single monster of that type for a quest.  Therefore, you *might* already have that Name when the quest is given.  As a result, Names can be endorsed by an NPC as well as given out by one.  An endorsement will increase that Name's power if you already have that Name.

#### Respect

NPCs have levels of interest.  If you are not respectable, since you haven't done much and therefore have no Name, you might be ignored by some NPCs and have to find simpler ones with easier quests.  As you build your Name, other NPCs will start to talk to you, eventually trusting you with bigger quests.

#### Battlecry

The Battlecry affects all enemies within earshot, which is a distance determined by how loudly you yell.  It permanently decreases stats of enemies if it is successful.  How successful it is depends on how loudly you yell and what the enemy is.  Your basic battlecry is just a shout, and affects all enemies equally.  As you gain Names, your battlecry can affect various types of enemies differently.  For instance, if your name includes Dragonsbane (because, for instance, you killed a bunch of dragons) then your battlecry will affect dragons more strongly.

### Skills

There is no levelling system per se.  You get better at the things you do more, with diminishing returns.  For instance, if you have a dagger and fight with it a lot, you increase your chances of hitting with the dagger, and increase your critical hit chance.  The weapon still does the same amount of damage (like, 1d4 base, for instance), but you get better at using it to inflict that damage.  This allows for there to be an advantage to sticking with a weaker weapon later in the game - if you are 100% effective with a 2d6 sword, but only 30% effective with a 3d8 axe, you'll be able to cause more damage with the sword.  

Also, you get better with weapons more quickly as you first start using them.  This makes sense - if you've never held a sword before, an hour of swinging it will give you the basics.  Similarly, you get diminishing returns as you go - it might take ten enemies to go from 30% hit chance to 75%, but then it would take a hundred to get from 75% to 80%.  Again, this makes sense - you get better quickly at first, but once you've got the basics down it takes long practice to get better.

It all goes back to one of my pet peeves with these games - equipment should be important, and not just discarded because you get something better.  

### Equipment

Equipment should be rare.  There might be only 5 weapons available in any one play through.  There will be many types of weapon, though, to make the playthroughs suitably unique.  For instance, the player might always start with a basic weapon - a knife, or a staff or a club or whatever, and some basic skill using it.  In order to get a stronger weapon there must be some effort.  It might be the crux of an entire quest to go and find a sword, for instance.

Armor is similarly difficult to work with, since it must be hand crafted to fit the player.  I expect that a good way to get around that is to make it enhanceable but the same armour all game.  Or, to find an armour maker who will create custom armour for a price/quest, and for a given time.  Something to make it so that you can't end the game carrying fifty sets of plate armour.

#### Enhancements

In order to offset the lack of equipment, there will be ways to enhance the equipment.  Much of this will involve words of power, and these might be learned through quests, or through books found in various locations after study.  This way, your equipment can get stronger.  For instance, using the word "sharpness" on the sword to create the "Sword of Sharpness" or something might make it a 2d6 + 1 sword.  

#### Charges

Some equipment, like rings, are inherently useless on their own.  Their use is to be imbued with spells.  Each item can hold only so many charges, and the spell must be the same.  Imbuing an item can only be done at Altars because the words that can imbue require too much Voice to be cast by a human.  An Altar channels the gods directly.  To simplify my life, when imbuing with such a word at an altar, the item is fully charged each time with no consequences.  Once it is imbued, the name of the item changes (Ring of Minor Healing + 3 - it can cast the Minor Heal spell 3 times).

Items that can be imbued can also be enhanced to hold more charges.  A very powerful enhancement would be to regenerate charges.  This will probably be a late-game enhancement that you get rarely.

#### Base weapons

Knife* - 1d3
Dagger* - 1d4
Club* - 1d4
Staff* - 1d6
Sword - 2d6
Axe - 2d8
Hammer - 3d6

\* player starts with one of these, with the dagger or club being most common.  Dagger and club are interchangeable and depend on the type of initial quest giver - if it's a chieftan, the player is a barbarian and gets the club.  Otherwise it's the dagger.  The knife and staff are both rarer, making the beginning game harder or easier.
