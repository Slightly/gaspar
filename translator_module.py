# -*- coding: utf-8 -*-
import urllib
import xml.etree.ElementTree as ET

apikey = 'trnsl.1.1.20170127T213415Z.fc36e7b9ace4fa05.ba1f446a83ebafe36aee5b5fba6f907bd4fe3c4f'

def Translate(text, language, source):
	if (not text and not language) or not language or not source or len(source) != 2:
		return 'Helyes szintaxis: !ytr [forrásnyelv] [célnyelv] [szöveg]'
	else:
		if len(language) != 2:
			text = language + ' ' +text
			source = source.lower()
			text = urllib.parse.quote(text)
			url = "https://translate.yandex.net/api/v1.5/tr/translate?key="+apikey+"&text="+text+"&lang="+source
		else:
			source = source.lower()
			language = language.lower()
			text = urllib.parse.quote(text)
			url = "https://translate.yandex.net/api/v1.5/tr/translate?key="+apikey+"&text="+text+"&lang="+source+'-'+language
		#url = urllib.parse.quote(url, safe='=&:/?')
		content = urllib.request.urlopen(url).read()
		root = ET.fromstring(content)
		response = root[0].text
#		print(response.encode('utf-8'))
		return response

def DoubleTranslate(src, med, txt):
	temp = Translate(txt, med, src)
	result = Translate(temp, src, med)
	return result