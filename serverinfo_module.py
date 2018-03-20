# -*- coding: utf-8 -*-
#Project finished - TODO: 4 db warningot kiszedni
import urllib
import xml.etree.ElementTree as ET
import os.path
import grammar
from bs4 import BeautifulSoup
import requests

global response
def GetServerDetails(servername):
	if servername.lower() not in ('tauri', 'wod', 'evermoon', 'tb', 'bb', 'alaris', 'ptr', 'mrgl'):
		global response1
		global response2
		response1 = 'Nincs ilyen szerver'
		response2 = ''
		return response1, response2
	content = urllib.request.urlopen("http://tauriwow.com/files/serverstatus.php").read()
	root = ET.fromstring(content)

	def CalculatePercentage(particle, total):
		try: 
			x = float(particle) / float(total) * 100
			return x
		except ZeroDivisionError:
			return 0
	def GetRealmProperName(serverid):
		return root[0][serverid][2].text
	
	def GetServerPopulation(serverid):
		return int(root[0][serverid][5].text)
	
	def GetServerOnlinestatus(serverid):
		return root[0][serverid][6].text
	
	def GetServerAlliancePopulation(serverid):
		return float(root[0][serverid][8].text)
	
	def GetServerHordePopulation(serverid):
		return float(root[0][serverid][9].text)

	def GetNeutralPopulation(realmid):
		return float(root[0][realmid][10].text)

	server =  {
	'tauri'	: 	0,
	'reborn': 	1,
	'wod'	: 	2,
	'tb' 	: 	3,
	'bb' 	: 	4,
	'alaris': 	5,
	'ptr'	: 	6,
	'evermoon': 7,
	'mrgl'	:	8
	}
	choice = servername.lower()
	realmProperName = GetRealmProperName(server[choice])
	serverstatus = GetServerOnlinestatus(server[choice])
	population = GetServerPopulation(server[choice])
	alliplayers = int(GetServerAlliancePopulation(server[choice]))
	hordaplayers = int(GetServerHordePopulation(server[choice]))
	allipercent = CalculatePercentage(alliplayers, population)
	hordapercent = CalculatePercentage(hordaplayers, population)
	neutralplayers = int(GetNeutralPopulation(server[choice]))
	neutralpct = float(CalculatePercentage(neutralplayers, population))


	if serverstatus == 'Online':
		response1 = ("\x039Van.")
		if server != server[choice] not in (8, 5, 4, 3):
			response2 = ("\x0307"+"%s Player játszik. \x0312Alliance: %s (%.1f %%) \x03| \x034Horde: %s (%.1f %%) | \x033Neutral: %s (%.1f %%)" % (population, alliplayers, allipercent, hordaplayers, hordapercent, neutralplayers, neutralpct))	
		else:
			response2 = ("\x0307"+"%s Player játszik. \x0312Alliance: %s (%.1f %%) \x03| \x034Horde: %s (%.1f %%)" % (population, alliplayers, allipercent, hordaplayers, hordapercent))
	else:
		response1 = ("Nincs")
		response2 = ""
	return response1, response2

def GetCollectiveDetails():
	servers = ["" for x in range(9)]
	playercount = ["" for x in range(9)]
	serverstatus = ["" for x in range(9)]
	article = ['' for x in range(9)]
	IsInactive = ['' for x in range(9)]

	content = urllib.request.urlopen("http://tauriwow.com/files/serverstatus.php").read()
	root = ET.fromstring(content)

	def GetRealmProperName(serverid):
		return root[0][serverid][2].text
	
	def GetServerPopulation(serverid):
		return int(root[0][serverid][5].text)
	
	def GetServerOnlinestatus(serverid):
		return root[0][serverid][6].text

	def IsInactiveServer(serverid):
		return root[0][serverid][12].text

	for i in range(0,9):
		servers[i] = GetRealmProperName(i)
		playercount[i] = str(GetServerPopulation(i))
		serverstatus[i] = GetServerOnlinestatus(i)
		IsInactive[i] = IsInactiveServer(i)
		article[i] = grammar.GetArticle(servers[i])
		if serverstatus[i] == 'Offline':		#Tauri wunderbar megoldása miatt ilyenkor az utoljára mért playerszámot mutatná
			playercount[i] = '0'

	response = ''
	Realms = [[0 for x in range(3)] for y in range(9)] 
	for i in range(0,9):
		Realms[i][0] = servers[i]
		Realms[i][1] = serverstatus[i]
		Realms[i][2] = int(playercount[i])
	for i in range(0,9):
		if IsInactive[i] == 'true':
			del(Realms[i])

	Realms = sorted(sorted(Realms, key = lambda y : y[1], reverse = True), key = lambda x : x[2], reverse=True)

	for i in range(len(Realms)):
		if Realms[i][1] == 'Online':
			Realms[i][1] = "\x039Online"
		else:
			Realms[i][1] = "\x034Offline" 

		Realms[i][0] = str(Realms[i][0])
		Realms[i][1] = str(Realms[i][1])
		Realms[i][2] = str(Realms[i][2])
		response += "\x037 %s: %s\x037 (%s) | " % (Realms[i][0], Realms[i][1], Realms[i][2])


	#for i in range(0,9):
	#	if IsInactive[i] != 'true':
	#		if serverstatus[i] == 'Online' and playercount[i] != '0':
	#			if serverstatus[i] == "Online":
	#				serverstatus[i] = "\x039Online"
	#			else:
	#				serverstatus[i] = "\x034Offline"
	#			response += "\x037" + servers[i] + ': ' +serverstatus[i] + '\x037 (' + playercount[i] + ') | '

	totalpop = 0
	for j in range(0,9):
		serverstatus[j] = GetServerOnlinestatus(j)
		if serverstatus[j] != 'Offline':
			totalpop += int(GetServerPopulation(j))
	response += ('Összesen: %d' % totalpop)
	#print(response)
	if totalpop == 0:
		response = 'Hibás adatok az xml-ben, blame Chris'
	return response

def GetPageTitle(page):
	try:
		soup = BeautifulSoup(urllib.request.urlopen(page))
		return soup.title.string
	except:
		try:
			x = 'http://'
			x = x+page
			print(x)
			soup = BeautifulSoup(urllib.request.urlopen(x))
			return soup.title.string
		except:
			return 'Nincs ilyen oldal.'

def GetResponseStatus(page):
	try:
		r = requests.head(page)
		if int(r.status_code) < 400:
			response = '%s is up' % page
		elif int(r.status_code) > 399 and int(r.status_code) < 500:
			response = "%s is unreachable (%d)" % (page, int(r.status_code))
		else:
			response = '%s is down (%d)' % (page, int(r.status_code))
		return response
	except:
		try:
			x = 'http://'
			x = x+page
			r = requests.head(x)
			if int(r.status_code) < 400:
				response = '%s is up' % page
			elif int(r.status_code) > 399 and int(r.status_code) < 500:
				response = "%s is unreachable (%d)" % (page, int(r.status_code))
			else:
				response = '%s is down (%d)' % (page, int(r.status_code))
			return response
		except requests.ConnectionError:
		    return ("Nincs ilyen oldal")
