from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import xml.etree.ElementTree as ET
import urllib


def MeasureDistance(city1, city2):
	geolocator = Nominatim()
	loc1 = geolocator.geocode(city1)
	loc2 = geolocator.geocode(city2)
	distance = vincenty((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).kilometers
	if distance <= 5:
		distance = vincenty((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).meters
		distance = 'A távolság %d méter.' % distance
	else:
		distance = 'A távolság %d km.' % distance
	return distance

def GetLocation(city):
	geolocator = Nominatim()
	location = geolocator.geocode(city)
	link = ('https://www.google.hu/maps/@%.7f,%.7f,15z' % (location.latitude, location.longitude))
	print(link)
	return link

def GetIPLocation(ip):
	try:
		content = urllib.request.urlopen("http://freegeoip.net/xml/%s"%ip).read()
		root = ET.fromstring(content)
		country = root[2].text
		city = root[5].text
		print('aaaa'+city)
		TZ = root[7].text
		print(TZ)
		if city == '' or str(city) == 'None' or type(city) == None:
			city = TZ
			print('fasz')
		response = "%s, %s" % (city, country)
	except:
		response = 'Ez nem mibbites nick.'
	return response
