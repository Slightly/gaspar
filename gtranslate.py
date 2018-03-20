import googletrans

def Translate(src, tar, txt):
	if (not txt and not tar) or not tar or not src or len(src) != 2:
		return 'Helyes szintaxis: !ytr [forrásnyelv] [célnyelv] [szöveg]'
	else:
		if len(tar) != 2:
			txt = tar + ' ' +txt
			tar = src.lower()
			TR = googletrans.Translator()
			result = TR.translate(txt, dest=tar).text
			return result
		else:
			src = src.lower()
			tar = tar.lower()
			TR = googletrans.Translator()
			result = TR.translate(txt, dest=tar, src=src).text
			print(src)
			print(tar)
			print(txt)
			return result

def Detect(what):
	TR = googletrans.Translator()
	lang = TR.detect(what).lang
	percent = TR.detect(what).confidence*100
	try:
		result = ('Ez a szöveg szerintem %s nyelven íródott. (%d%% valószínűség)' % (langs[lang].lower(), percent))
	except:
		result = 'Nem tudom pontosan, milyen nyelven íródott.'
	finally:
		return result


langs = {
	'af' : 'Afrkiaans',
	'sq' : 'Albán',
	'am' : 'Amhár',
	'ar' : 'Arab',
	'hy' : 'Örmény',
	'az' : 'Azeri',
	'eu' : 'Baszk',
	'be' : 'Fehérorosz',
	'bg' : 'Bolgár',
	'bn' : 'Bengáli',
	'bs' : 'Boszniai', 
	'ca' : 'Katalán',
	'ceb':	'Cebuano',
	'zh-cn': 'Egyszerű kínai',
	'zh-tw':	'Hagyományos kínai',
	'co'	:	'Korzikai',
	'hr'	:	'Horvát',
	'cs'	:	'Cseh',
	'da'	:	'Dán',
	'nl'	:	'Holland',
	'en'	:	'Angol',
	'eo'	:	'Eszperantó',
	'et'	:	'Észt',
	'fi'	:	'Finn',
	'fr'	:	'Francia',
	'fy'	:	'Fríz',
	'gl'	:	'Gallíciai',
	'ka'	:	'Grúz',
	'de'	:	'Német',
	'el'	:	'Görög',
	'gu'	:	'Gujarati',
	'ht'	:	'Haiti kreol',
	'ha'	:	'Hausa',
	'haw'	:	'Hawaii',
	'iw'	:	'Héber',
	'hi'	:	'Hindi',
	'hmn'	:	'Hmong',
	'hu'	:	'Magyar',
	'is'	:	'Izlandi',
	'ig'	:	'Igbo',
	'id'	:	'Indonéz',
	'ga'	:	'Ír',
	'it'	:	'Olasz',
	'ja'	:	'Japán',
	'jw'	:	'Jávai',
	'kn'	:	'Kannada',
	'kk'	:	'Kazah',
	'km'	:	'Khmer',
	'ko'	:	'Koreai',
	'ku'	:	'Kurd',
	'ky'	:	'Kirgiz',
	'lo'	:	'Laoszi',
	'la'	:	'Latin',
	'lv'	:	'Lett',
	'lt'	:	'Litván',
	'lb'	:	'Luxemburgi',
	'mk'	:	'Macedón',
	'mg'	:	'Malagasy',
	'ms'	:	'Maláj',
	'ml'	:	'Malayalam',
	'mt'	:	'Máltai',
	'mi'	:	'Maori',
	'mr'	:	'Marathi',
	'mn'	:	'Mongol',
	'my'	:	'Burmai',
	'ne'	:	'Nepáli',
	'no'	:	'Norvég',
	'ny'	:	'Nyanja',
	'ps'	:	'Pashto',
	'fa'	:	'Perzsa',
	'pl'	:	'Lengyel',
	'pt'	:	'Portugál',
	'pa'	:	'Punjabi',
	'ro'	:	'Román',
	'ru'	:	'Orosz',
	'sm'	:	'Szamoai',
	'gd'	:	'Skót',
	'sr'	:	'Szerb',
	'st'	:	'Sesotho',
	'sn'	:	'Shona',
	'sd'	:	'Sindhi',
	'si'	:	'Szingaléz',
	'sk'	:	'Szlovák',
	'sl'	:	'Szlovén',
	'so'	:	'Szomáli',
	'es'	:	'Spanyol',
	'su'	:	'Szudáni',
	'sw'	:	'Szuahéli',
	'sv'	:	'Svéd',
	'tl'	:	'Tagalog',
	'tg'	:	'Tádzsik',
	'ta'	:	'Tamil',
	'te'	:	'Telugu',
	'th'	:	'Thai',
	'tr'	:	'Török',
	'uk'	:	'Ukrán',
	'ur'	:	'Urdu',
	'uz'	:	'Üzbég',
	'vi'	:	'Vietnámi',
	'cy'	:	'Walesi',
	'xh'	:	'Xhosa',
	'yi'	:	'Jiddish',
	'yo'	:	'Yoruba',
	'zu'	:	'Zulu'
}
