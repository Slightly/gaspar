# -*- coding: utf-8 -*-
import wikipedia #Note: Ez egy otromba gusztustalan modul, nem lehet szebben megírni a lekérdezéseket.

def Search(query):
	#wikipedia.set_lang('en')
	#if type(query) == str:
	#	tmp = query.split()
	#	if len(tmp[0]) == 2 and len(tmp) != 1:
	#		query = query.split(' ', 1)[1]
	#		print('Queryh '+query)
	#		query = query.strip("'")
	#		wikipedia.set_lang(tmp[0])
	#		print('Final Query: '+query)
	#	try:
	#		result = wikipedia.summary(query, sentences=4, auto_suggest=True)
	#	except wikipedia.exceptions.DisambiguationError as error:
	#		print('Itt lett volna egy exception')
	#		try:
	#			result = wikipedia.summary(error.args[1][1], sentences=4, auto_suggest=True)
	#		except:
	#			result = 'Több ilyen szócikket találtam, kérlek pontosíts!'
	#		#print(result)
	#	except wikipedia.exceptions.PageError:
	#		try:															#Hátha valaki nab és elfelejti, hogy angolul keres alapból
	#			wikipedia.set_lang('hu')
	#			result = wikipedia.summary(query, sentences=4, auto_suggest=True)
	#		except wikipedia.exceptions.DisambiguationError as error:
	#			print('Itt lett volna egy exception')
	#			try:
	#				result = wikipedia.summary(error.args[1][1], sentences=4, auto_suggest=True)
	#			except:
	#				result = 'Több ilyen szócikket találtam, kérlek pontosíts!'
	#		except:
	#			result = 'Nem találtam ilyen szócikket'
	#	except:
	#		result = 'Caught an exception'
	#	return result
	return ''
#Temp disabled

#def SummarizeLink(link):

