#!/usr/bin/env python

from bs4 import BeautifulSoup
import glob
import json
import os
import errno

#############################################
# Convert Hearthstone card data XML to JSON #
#############################################

__author__ = "Taylor Caldwell - http://github.com/rithms"
__copyright__ = "Copyright 2015, Taylor Caldwell"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Taylor Caldwell"
__email__ = "tcaldwel@nmsu.edu"
__status__ = "Production"
 
# EnumIds - Non-Boolean
enum_dict = {
    
	45 : "health",
	47 : "attack",
	48 : "cost",
	183 : "cardSet",
	184 : "cardTextInHand",
	185 : "cardName",
	187 : "durability",
	199 : "class",
	200 : "race",
	201 : "faction",
	202 : "cardType",
	203 : "rarity",
	251 : "attackVisualType",
	252 : "cardTextInPlay",
	268 : "devState",
	325 : "targetingArrowText",
	330 : "enchantmentBirthVisual",
	331 : "enchantmentIdleVisual",
	342 : "artistName",
	351 : "flavorText",
	365 : "howToGetThisGoldCard",
	364 : "howToGetThisCard",
	#377 : "unknownHasOnDrawEffect",
	#380 : "unknownBlackrockHeroes",
	#389 : "unknownDuneMaulShaman",
	#402 : "unknownIntenseGaze",
	#401 : "unknownBroodAffliction"
}

# EnumIds - Boolean
bool_dict = {

	32 : "Trigger Visual",
	114 : "elite",	
	321 : "collectible",
	189 : "Windfury",
	190 : "Taunt",
	191 : "Stealth",
	192 : "Spell Power",
	194 : "Divine Shield",
	197 : "Charge",
	205 : "Summoned",
	208 : "Freeze",
	212 : "Enrage",
	215 : "Overload",
	217 : "Deathrattle",
	218 : "Battlecry",
	219 : "Secret",
	220 : "Combo",
	240 : "Can't Be Damaged",
	293 : "Morph",
	335 : "Invisible Deathrattle",
	338 : "One Turn Effect",
	339 : "Silence",
	340 : "Counter",
	349 : "Immune To Spell Power",
	350 : "Adjacent Buff",
	361 : "Heal Target",
	362 : "Aura",
	363 : "Poisonous",
	367 : "AI Must Play",
	370 : "Affected By Spell Power",
	388 : "Spare Part",
}

# Card Class IDs
class_dict = {

	0 : "Developer",
	2 : "Druid",
	3 : "Hunter",
	4 : "Mage",
	5 : "Paladin",
	6 : "Priest",
	7 : "Rogue",
	8 : "Shaman",
	9 : "Warlock",
	10 : "Warrior",
	11 : "Dream"
}

# Card Set IDs
set_dict = {

	2 : "Basic",
	3 : "Classic",
	4 : "Reward",
	5 : "Missions",
	7 : "System",
	8 : "Debug",
	11 : "Promotion",
	12 : "Curse of Naxxramas",
	13 : "Goblin vs Gnomes",
	14 : "Blackrock Mountain",
	16 : "Credits"
}

# Card Type IDs
type_dict = {

	3 : "Hero",
	4 : "Minion",
	5 : "Spell",
	6 : "Enchantment",
	7 : "Weapon",
	10 : "Hero Power"
}

# Card Race IDs
race_dict = {

	14 : "Murloc",
	15 : "Demon",
	17 : "Mechanical",
	20 : "Beast",
	21 : "Totem",
	23 : "Pirate",
	24 : "Dragon"
}

# Card Faction IDs
faction_dict = {

	1 : "Horde",
	2 : "Alliance",
	3 : "Neutral"
}

# Card Rarity IDs
rarity_dict = {

	0 : "Developer",
	1 : "Common",
	2 : "Free",
	3 : "Rare",
	4 : "Epic",
	5 : "Legendary"
}

# Map int value to its meaning using the dict its field corresponds to
def get_value(enum_id, field):
	if field == 'class':
		d = class_dict
	elif field == 'cardSet':
		d = set_dict
	elif field == 'cardType':
		d = type_dict
	elif field == 'race':
		d = race_dict
	elif field == 'faction':
		d = faction_dict
	elif field == 'rarity':
		d = rarity_dict
	else:
		return enum_id
	if enum_id in d:
		return d[enum_id]

# Add string value from xml to data dict
def add_string_value_to_dict(d, card_id, enum_id, value):
	if enum_id in enum_dict:
		d['data'][card_id][enum_dict[enum_id]] = value

# Give int value from xml meaning, and add to data dict
def add_int_value_to_dict(d, card_id, enum_id, value):
	if enum_id in enum_dict:
		field = enum_dict[enum_id]
		value = get_value(int(value), field)
		d['data'][card_id][enum_dict[enum_id]] = value

	elif enum_id in bool_dict:
		field = bool_dict[enum_id]
		if field == 'collectible' or field == 'elite':
			if value == '1':
				d['data'][card_id][field] = True
			elif value == '0':
				d['data'][card_id][field] = False
		else:
			if value == '1':
				d['data'][card_id]['mechanics'].append(field)

# If card doesn't have a collectible or elite field, add that field and set the value to false
def fill_missing_boolean_values(card_id, json_dict):
	for key in bool_dict:
		field = bool_dict[key]
		if field == 'collectible' or field == 'elite':
			if field not in json_dict['data'][card_id]:
				json_dict['data'][card_id][field] = False

# Remove HTML and variable tags from text
def remove_tags(text):
	tags=['<b>', '</b>', '<i>', '</i>', '$', '#']
	for tag in tags:
		text = text.replace(tag, '')
	return text

# Add locale value to card data
def add_locale(locale, card_id, json_dict):
	data = json_dict['data'][card_id]
	data['locale'] = locale

# Add image and premium image to card data (credits to ZAM for extracted images)
def add_images(locale, card_id, json_dict):
	data = json_dict['data'][card_id]
	if data['id'][-1] != 'o':
		card_id = data['id']
		data['image'] = 'http://wow.zamimg.com/images/hearthstone/cards/' + locale.lower() + '/original/' + card_id + '.png'
		data['goldImage'] = 'http://wow.zamimg.com/images/hearthstone/cards/' + locale.lower() + '/animated/' + card_id + '_premium.gif'

# Clean the text fields found in the data by removing the HTML tags
def clean_text(card_id, json_dict):
	data = json_dict['data'][card_id]
	if 'cardTextInHand' in data:
		text = data['cardTextInHand']
		data['cardTextInHand'] = remove_tags(text)
	if 'flavorText' in data:
		text = data['flavorText']
		data['flavorText'] = remove_tags(text)
	if 'targetingArrowText' in data:
		text = data['targetingArrowText']
		data['targetingArrowText'] = remove_tags(text)

# Make sure path exists - duh
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Write json data to json file
def write_to_file(file_name, data):
	with open('json/'+file_name+'.json', 'w') as outfile:
			json.dump(data, outfile, sort_keys=True)

# Convert XML card data to json and add to json_dict
def convert(card, locale, json_dict):
	card_id = card.get('CardID')
	json_dict['data'][card_id] = { 'id' : card_id, 'mechanics' : [] }

	# Convert all tags found in XML to JSON fields and values
	tags = card.find_all('Tag')
	for tag in tags:
		enum_id = int(tag.get('enumID'))
		if(tag.get('type') == 'String'):
			value = tag.text
			add_string_value_to_dict(json_dict, card_id, enum_id, value)
		else:
			value = tag.get('value')
			add_int_value_to_dict(json_dict, card_id, enum_id, value)

	fill_missing_boolean_values(card_id, json_dict)

	# Remove mechanics field from dict if card does not have any mechanics
	if not json_dict['data'][card_id]['mechanics']:
		del json_dict['data'][card_id]['mechanics']

	add_locale(locale, card_id, json_dict)
	add_images(locale, card_id, json_dict)
	clean_text(card_id, json_dict)


# Run script
def run():
	make_sure_path_exists('json/') # Create json dir
	for f in glob.glob('cardxml0/CAB-cardxml0/TextAsset/*.txt'): # open all xml files
		with open(f) as cardfile:
			file_name = f.split('/')[-1].split('.')[0]
			cardsoup = BeautifulSoup(cardfile.read(), features="xml")
	 
		cards = cardsoup.find_all('Entity')
		json_dict = { 'data' : {} }

		for card in cards:	# for every card in xml file, convert to json
			convert(card, file_name, json_dict)
		write_to_file(file_name, json_dict) # write json to file

run()
 




