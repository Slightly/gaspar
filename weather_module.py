# -*- coding: utf-8 -*-
import pyowm
import datetime
from time import sleep as Wait

owm = pyowm.OWM('c2773b82d7ca7abef1f0da9e31863883', language='hu') #Szupertitkos API kulcs

def UpdateWeather(place):							#Adatok letöltése/frissítése
	#try:
	#	observation = owm.weather_at_place(place)
	#except:
	#	line1 = "Baj van az API-val vagy hibás helységnevet adtál meg."
	#	line2 = ''
	#	print('API HIBA')
	#	return line1, line2
	observation = owm.weather_at_place(place)
	print(observation)
	weather = observation.get_weather()
	location = observation.get_location()
	return weather, location					


def GetWeatherData(place):							#Ez határozza meg, hogy az UpdateWeather() milyen helyről kérje le az infót
	print(place)
	weather, location = UpdateWeather(place)
	if place == '' or len(place) < 2:
		line1 = 'Használat: !weather [helységnév]'
		line2 = ''
		return line1, line2
	if type(weather) == str:
		return 'API hiba', ''
	#place = place.replace('á', 'a')
	#place = place.replace('é', 'e')
	#place = place.replace('í', 'i')
	#place = place.replace('ó', 'o')
	#place = place.replace('ö', 'o')
	#place = place.replace('ő', 'o')
	#place = place.replace('ú', 'u')
	#place = place.replace('ü', 'u')
	#place = place.replace('ű', 'u')
	weather, location = UpdateWeather(place)
	wind_dir = ' '
	try:
		wind_dir_deg = weather.get_wind()['deg'] 	#Mert undormány az API, és ha nem tud deg-et mondani, akkor annyit se mond, hogy húzd meg a faszom, csak exceptiont dob
	except:
		print('Hiba: Nem sikerült megállapítani a szélirányt.')
	else:
		if wind_dir_deg > 337 or wind_dir_deg <= 22:
			wind_dir = 'Északi'
		elif wind_dir_deg > 22 and wind_dir_deg <= 67:
			wind_dir = 'Északkeleti'
		elif wind_dir_deg > 67 and wind_dir_deg <= 112:
			wind_dir = 'Keleti'
		elif wind_dir_deg > 112 and wind_dir_deg <= 157:
			wind_dir = 'Délkeleti'
		elif wind_dir_deg > 157 and wind_dir_deg <= 202:
			wind_dir = 'Déli'
		elif wind_dir_deg > 202 and wind_dir_deg <= 247:
			wind_dir = 'Délnyugati'
		elif wind_dir_deg > 247 and wind_dir_deg <= 292:
			wind_dir = 'Nyugati'
		elif wind_dir_deg > 292 and wind_dir_deg <= 337:
			wind_dir = 'Északnyugati'

	#Favágás 
	basetime = weather.get_reference_time('iso')
	basetime = basetime.replace(' ', '')[:-3]
	basetime = datetime.datetime.strptime(basetime, "%Y-%m-%d%H:%M:%S")
	basetime += datetime.timedelta(hours=1) #DST == 2 
	basetime = str(basetime)
	
	line1 = ('%s időjárás információ | Frissítve: %s | %s | Hőmérséklet: %d °C' % (location.get_name(), basetime, weather.get_detailed_status(), round(weather.get_temperature('celsius')['temp'])))
	line2 = ('Légnyomás: %d hPa | Páratartalom: %d %% | Szél: %d km/h, %s' % (weather.get_pressure()['press'], weather.get_humidity(), round(weather.get_wind()['speed']*3.6), wind_dir))
	place = ''
	return line1, line2


def GetForecast(city, days):			#TODO: Weather_at implementáció (datetime-ot kell baszkodni hozzá)
	if  days in ('1', '2', '3', '4', '5'):
		days = int(days)
		if days < 6:
			try:
				forecasts	=	owm.daily_forecast(city)
			except:
				return 'Nincs ilyen város'
			forecast 	= 	forecasts.get_forecast()
			weather 	= 	forecast.get_weathers()
			location 	= 	forecast.get_location()
			date 		= 	forecasts.when_starts('date')
			date 		+=	datetime.timedelta(days=days)
			date 		=	str(date)[:-15]
			weather 	= 	weather[days]
			line = ('Előrejelzés %s területére %s napra: %s | Minimum/maximum: %d/%d °C' % (location.get_name(), date, weather.get_detailed_status(), round(weather.get_temperature('celsius')['min']), weather.get_temperature('celsius')['max']))
			return line
		else:
			return 'Nincs előrejelzésem erre a napra.'
	elif days.find('hr') != -1:
		try:
			forecasts = owm.three_hours_forecast(city)
		except:
			return 'Nincs ilyen város'
		hrs = days[:-2]
		hrs = round(int(hrs)/3)
		if hrs > 15:
			return '5 napnál kevesebb időt adj meg'
		#print("daycount "+hrs)
		forecast = forecasts.get_forecast()
		location = forecast.get_location()
		weather = forecast.get_weathers()
		weather = weather[hrs] # x*3hr-es forecastnál ez majd a 3 egész osztója legyen
		if hrs == 0:
			hrs = 1
		line = ('%d órás előrejelzés %s területére: %s, %d °C' % (hrs*3, location.get_name(), weather.get_detailed_status(), round(weather.get_temperature('celsius')['temp'])))
		return line
	else:
		return ''		

GodxCities = ('Budapest', 'Debrecen', 'Győr', 'Makó', 'Mohács', 'Szeged', 'Ulm')

def GetGodxUpdate():
	response = 'GodX időjárás: '
	GodxWeather = [[0 for x in range(3)] for y in range(7)] 
	for i in range(len(GodxCities)):
		try:
			weather, loc = UpdateWeather(GodxCities[i])
		except:
			return 'API hiba'
			break
		if type(weather) != str:
			GodxWeather[i][0] = weather.get_detailed_status()
			GodxWeather[i][1] = int(round(weather.get_temperature('celsius')['temp']))
			GodxWeather[i][2] = GodxCities[i] #Favágás, majd legyen szebb
			Wait(1)
			#import operator
			#GodxWeather = sorted(GodxWeather, key = operator.itemgetter(1, 2))
		else:
			return "API hiba"
			break
	GodxWeather = sorted(sorted(GodxWeather, key = lambda x : x[2]), key = lambda y : y[1])  	
	for i in range(len(GodxCities)):
				response += '%s: %s, %d °C | ' % (GodxWeather[i][2], GodxWeather[i][0], GodxWeather[i][1])	
	response = response[:-2] # Whitespace és | levágása
	return response

def GetNextRain(city):
	try:
		forecasts	=	owm.three_hours_forecast(city)
	except:
		return 'Nincs ilyen város'
	allrains = forecasts.when_rain() # Később akár ki lehet szedni a többi napot is
	if len(allrains) > 0:
		firstrain 	=	allrains[0].get_reference_time('date')
		firstrain 	+= datetime.timedelta(hours=1) #DST == 2 
		firstrain 	=	str(firstrain)[:-9]
		response 	= 	('A következő eső ekkor várható: %s' % firstrain)
	else:
		response	=	'Nem várható eső a következő 5 napban.'
	return response

def GetNextSnow(city):
	try:
		forecasts	=	owm.three_hours_forecast(city)
	except:
		return 'Nincs ilyen város'
	allsnows = forecasts.when_snow() # Később akár ki lehet szedni a többi napot is
	if len(allsnows) > 0:
		firstsnow 	= 	allsnows[0].get_reference_time('date')
		firstsnow   += datetime.timedelta(hours=1) #DST == 2 
		firstsnow 	= 	str(firstsnow)[:-9]
		response 	= 	('A következő havazás ekkor várható: %s' % firstsnow)
	else:
		response	= 	'Nem várható havazás a következő 5 napban.'
	return response

def GetNextClear(city):
	try:
		forecasts	=	owm.three_hours_forecast(city)
	except:
		return 'Nincs ilyen város'
	allsnows = forecasts.when_clear() # Később akár ki lehet szedni a többi napot is
	if len(allsnows) > 0:
		firstsnow 	= 	allsnows[0].get_reference_time('date')
		firstsnow   += datetime.timedelta(hours=1) #DST == 2 
		firstsnow 	= 	str(firstsnow)[:-9]
		response 	= 	('A következő derűs idő ekkor várható: %s' % firstsnow)
	else:
		response	= 	'Nem várható derűs idő a következő 5 napban.'
	return response

def GetNextStorm(city):
	try:
		forecasts	=	owm.three_hours_forecast(city)
	except:
		return 'Nincs ilyen város'
	allsnows = forecasts.when_storm() # Később akár ki lehet szedni a többi napot is
	if len(allsnows) > 0:
		firstsnow 	= 	allsnows[0].get_reference_time('date')
		firstsnow   += datetime.timedelta(hours=1) #DST == 2 
		firstsnow 	= 	str(firstsnow)[:-9]
		response 	= 	('A következő vihar ekkor várható: %s' % firstsnow)
	else:
		response	= 	'Nem várható vihar a következő 5 napban.'
	return response

def CheckIfRain(city, time):#Ez egyelőre disabled, mert 1) Nincs megoldva a város-idő dualitás 2) Valahogy meg kell győzni, hogy jó datetime-ot kap 3) Lehet, hogy nem is működik a feature 
	return 'NYI'
#	try:
#		forecasts = owm.three_hours_forecast(city)
#	except:
#		return 'Nincs ilyen város'
#	time += ' 00:00:00+00'
#	WillItRain = forecasts.will_be_rainy_at(time)
#	if WillItRain == True:
#		response = 'Várható eső a megadott időpontban'
#	else:
#		response = 'Nem várható eső a megadott időpontban'
#	return response