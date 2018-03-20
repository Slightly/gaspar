# -*- coding: utf-8 -*-
vowels = ('a', 'á', 'e', 'é', 'i', 'í', 'o', 'ó', 'ö', 'ő', 'u', 'ú', 'ü', 'ű')
deepVowels = ('a', 'á', 'o', 'ó', 'u', 'ú')
shortVowels = ('a', 'e', 'i', 'o', 'ö', 'u', 'ü')
longVowels = ('á', 'é', 'í', 'ó', 'ő', 'ú', 'ű')

colors = {
    'COLOR_WHITE'         :   0,
    'COLOR_BLACK'         :   1,
    'COLOR_DBLUE'     	  :   2,
    'COLOR_DGREEN'   	  :   3,
    'COLOR_RED'		 	  :   4,   
    'COLOR_DRED'    	  :   5,
    'COLOR_DVIOLET'    	  :   6,
    'COLOR_ORANGE'   	  :	  7,
    'COLOR_YELLOW'    	  :   8,
    'COLOR_LGREEN'    	  :   9,
    'COLOR_CYAN'  		  :  10,
    'COLOR_LCYAN'     	  :  11,
    'COLOR_BLUE'   		  :  12,
    'COLOR_VIOLET'        :  13,
    'COLOR_DGRAY'   	  :  14,
    'COLOR_LGRAY'    	  :  15
}


'''
#IRC FORMATTING

enum ControlCode {
    Bold            = 0x02,     /**< Bold */
    Color           = 0x03,     /**< Color */
    Italic          = 0x09,     /**< Italic */
    StrikeThrough           = 0x13,     /**< Strike-Through */
    Reset           = 0x0f,     /**< Reset */
    Underline       = 0x15,     /**< Underline */
    Underline2      = 0x1f,     /**< Underline */
    Reverse         = 0x16      /**< Reverse */
};
'''


def GetLongVowel(letter):
	if letter not in vowels or letter in longVowels:
		pass
	else:
		for i in range(len(shortVowels)):
			if shortVowels[i] == letter:
				letter = longVowels[i]
	return letter

def GetDativeForm(word): # -nak/-nek
	lastVowel = ''
	for i in range(len(word)):
		if word[i].lower() in vowels:
			lastVowel = word[i]
	if word[-1:].lower() in shortVowels and word[-1:].lower() not in ('u', 'ü', 'i'): #Mgh megnyúlás, pl. Emese -> Emesének
		vowel = GetLongVowel(word[-1:])
		word = word[:len(word)-1] + vowel
	if lastVowel == '':
		print('Nonexistent dative error (no vowels found)')
	elif lastVowel in deepVowels:
		word += 'nak'
	else:
		word += 'nek'
	return word

def GetArticle(word):
	if word[0].lower() not in vowels:
		return 'A'
	else:
		return 'Az'

#def ColorizeText(text, color):		Nem működik
#	colorstring = "\\0x"+ str(colors[color])
#	print(colorstring)
#	text = colorstring+text
#	print(text)
#	return text