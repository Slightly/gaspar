# -*- coding: utf-8 -*-
def GetZone(level): 
	suitable_zones_A = 'Alli: '
	suitable_zones_H = ' Horda: '
	suitable_zones = ' Contested: '

	try:
		level = int(level)
	except:
		return "Hibás szintaxis."

	if level >= 1 and level < 11:
		suitable_zones = 'Fajok kezdőterületei'
	if level >= 11 and level < 16:
		suitable_zones_A += 'Westfall | '
	if level >= 11 and level < 21:
		suitable_zones_A += 'Bloodmyst Isle | Loch Modan | Darkshore | '
		suitable_zones_H += 'Azshara | Ghostlands | Northern Barrens | Silverpine Forest | '
	if level >= 15 and level < 21:
		suitable_zones_A += 'Redridge Mountains | '
	if level >= 20 and level < 26:
		suitable_zones_A += 'Duskwood | Wetlands | '
		suitable_zones_H += 'Hillsbrad Foorhills | Ashenvale | '
	if level >= 25 and level < 31:
		suitable_zones += 'Arathi Highlands | Northern Stranglethorn | Stonetalon Mountains | '
	if level >= 30 and level < 36:
		suitable_zones += 'Cape of Stranglethorn | Desolace | Southern Barrens | Hinterlands | '
	if level >= 35 and level < 41:
		suitable_zones += 'Feralas | Dustwallow Marsh | Western Plaguelands | '
	if level >= 40 and level < 46:
		suitable_zones += 'Eastern Plaguelands | Thousand Needles | '
	if level >= 44 and level < 49:
		suitable_zones += 'Badlands | '
	if level >= 45 and level < 51:
		suitable_zones += 'Tanaris | Felwood | '
	if level >= 47 and level < 52:
		suitable_zones += 'Searing Gorge | '
	if level >= 49 and level < 53:
		suitable_zones += 'Burning Steppes | '
	if level >= 50 and level < 56:
		suitable_zones += 'Un\'Goro Crater | Winterspring | '
	if level >= 52 and level < 55:
		suitable_zones += 'Swamp of Sorrows | '
	if level >= 54 and level < 59:
		suitable_zones += 'Blasted Lands | '
	if level >= 55 and level < 59:
		suitable_zones += 'Moonglade | Deadwind Pass | Silithus | '
	if level >= 58 and level < 64:
		suitable_zones += 'Hellfire Peninsula | '
	if level >= 60 and level < 65:
		suitable_zones += 'Zangarmarsh | '
	if level >= 62 and level < 66:
		suitable_zones += 'Terokkar Forest | '
	if level >= 64 and level < 68:
		suitable_zones += 'Nagrand | '
	if level >= 65 and level < 69:
		suitable_zones += 'Blade\'s Edge Mountanins | '
	if level >= 67 and level < 71:
		suitable_zones += 'Netherstorm | Shadowmoon Valley | '
	if level == 70:
		suitable_zones += 'Isle of Quel\'Danas | '
	if level >= 68 and level < 73:
		suitable_zones += 'Borean Tundra | Howling Fjord | '
	if level >= 71 and level < 76:
		suitable_zones += 'Dragonblight | '
	if level >= 73 and level < 76:
		suitable_zones += 'Grizzly Hills | '
	if level >= 74 and level < 77:
		suitable_zones += 'Zul\'Drak | '
	if level >= 76 and level < 79:
		suitable_zones += 'Sholazar Basin | '
	if level >= 78 and level < 81:
		suitable_zones += 'Storm Peaks | Icecrown | Crystalsong Forest | '
	if level >= 80 and level < 83:
		suitable_zones += 'Vashj\'ir | Mount Hyjal | '
	if level >= 82 and level < 84:
		suitable_zones += 'Deepholm | '
	if level >= 83 and level < 85:
		suitable_zones += 'Uldum | '
	if level >= 84 and level < 86:
		suitable_zones += 'Twiligh Highlands | '
	if level >= 85 and level < 87:
		suitable_zones += 'Jade Forest | '
	if level >= 86 and level < 88:
		suitable_zones += 'Valley of the Four Winds | Kasarang Wilds | '
	if level >= 87 and level < 89:
		suitable_zones += 'Kun-Lai Summit | '
	if level >= 88 and level < 90:
		suitable_zones += 'Townlong Steppes | Dread Wastes | '
	if level == 90:
		suitable_zones = 'NYI'
	if level == 255:
		suitable_zones = 'GM Island'
	if level < 1 or level > 91 and level != 255:
		suitable_zones = 'Nincs ilyen szint'
	if suitable_zones_A == 'Alli: ':
		suitable_zones_A = ''
	if suitable_zones_H == ' Horda: ':
		suitable_zones_H = ''
	if suitable_zones == ' Contested: ':
		suitable_zones = ''
	real_zone = suitable_zones_A + suitable_zones_H + suitable_zones
	real_zone = real_zone.strip()
	return real_zone
