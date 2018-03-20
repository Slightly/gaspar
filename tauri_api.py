import requests
import json
import urllib

secret = 'ad684bd5d46e576ec1788b23d6375ba2bb1020df'
apikey = 'cba9f2c0000d3794'
RaceList = ["", "Human", "Orc", "Dwarf", "Night elf", "Undead", "Tauren", "Gnome", "Troll", "Goblin", "Blood elf", 'Draenei', '', '', '', '', '', '', '', '', '', '', 'Worgen', '']
ClassList = ['', 'Warrior', "Paladin", 'Hunter', 'Rogue', 'Priest', 'Death Kinght', 'Shaman', 'Mage', 'Warlock', 'Monk', 'Druid']


def GetCharacterData(char, realm):
	if realm.lower() == 'tauri':
		realm = '[HU] Tauri WoW Server'
	elif realm.lower() == 'wod':
		realm = '[HU] Warriors of Darkness'
	elif realm.lower() == 'evermoon':
		realm = '[EN] Evermoon'
	elif realm.lower() == 'bb':
		realm = '[EN] Burning Blade'
	else:
		realm = 'Error'

	validRealms = ('[HU] Tauri WoW Server', '[HU] Warriors of Darkness', '[EN] Evermoon', '[EN] Burning Blade')
	if realm in validRealms:
		try:
			payload = {'secret': secret, 'url': 'character-sheet', 'params': {'r': realm, 'n': char}}
			response = requests.post('http://chapi.tauri.hu/apiIndex.php?apikey='+apikey, data=json.dumps(payload), timeout=5)
			data = response.json()
		except:
			return 'Hiba', ''
		#
		try:
			name = data['response']['name']
		except:
			return 'Nincs ilyen karakter.', ''
		race = data['response']['race']
		p_class = data['response']['class']
		level = data['response']['level']
		guild = data['response']['guildName']
		if guild == '':
			guild = '-'
		gear = data['response']['characterItems']
		ilevel = 0
		pieces = 0
		for n in range(len(gear)):
			lvl = gear[n]['ilevel']
			ilevel += lvl
			if lvl > 1:	#Shirt meg tabard valamiért level 1 és elbasz mindent, thx blizz 
				pieces += 1
		if pieces > 0:
			ilevel = ilevel / pieces
		else:
			ilevel = 0
		talent1 = data['response']['treeName_0']
		talent2 = data['response']['treeName_1']
		if talent1 != '' and talent2 != '':
			talentdata = "%s | %s" % (talent1, talent2)
		elif talent1 == '' and talent2 != '':
			talentdata = "%s" % talent2
		elif talent1 != '' and talent2 == '':
			talentdata = "%s" % talent1
		else:
			talentdata = '-'
		try:
			prof1_name = data['response']['primary_trade_skill_1']['name'] # |Name, |value
			prof1_val = data['response']['primary_trade_skill_1']['value']
			prof1_data = "%s (%d)" % (prof1_name, prof1_val)
		except:
			prof1_data = '-'
		try:
			prof2_name = data['response']['primary_trade_skill_2']['name']
			prof2_val = data['response']['primary_trade_skill_2']['value']		
			prof2_data = "%s (%d)" % (prof2_name, prof2_val
	)
		except:
			prof2_data = '-'
		#
		result = "%s, Level %d %s %s | Guild: %s | Item Level: %d | Talent: %s | Profession: %s | %s" % (name, level, RaceList[race], ClassList[p_class], guild, ilevel, talentdata, prof1_data, prof2_data)
		link = "https://tauriwow.com/armory#character-sheet.xml?r=%s&n=%s" % (realm, name)
		link = urllib.parse.quote(link, safe=':/?=&#')
		return result, link
	else:
		return 'Ez a realm nem támogatott.', ''


def GetLinkToCharacter(char, realm):
	if realm.lower() == 'tauri':
		realm = '[HU] Tauri WoW Server'
	elif realm.lower() == 'wod':
		realm = '[HU] Warriors of Darkness'
	elif realm.lower() == 'evermoon':
		realm = '[EN] Evermoon'
	elif realm.lower() == 'bb':
		realm = '[EN] Burning Blade'
	else:
		realm = 'Error'

	validRealms = ('[HU] Tauri WoW Server', '[HU] Warriors of Darkness', '[EN] Evermoon')
	if realm in validRealms:
		try:
			payload = {'secret': secret, 'url': 'character-sheet', 'params': {'r': realm, 'n': char}}
			response = requests.post('http://chapi.tauri.hu/apiIndex.php?apikey='+apikey, data=json.dumps(payload), timeout=5)
			data = response.json()
		except:
			return 'API hiba'
		#
		try:
			name = data['response']['name']
		except:
			return 'Nincs ilyen karakter'
		link = "https://tauriwow.com/armory#character-sheet.xml?r=%s&n=%s" % (realm, name)
		link = urllib.parse.quote(link, safe=':/?=&#')
		return link
	else:
		return 'Nincs ilyen realm'
