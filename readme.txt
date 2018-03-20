UTILITY IRC BOT 1.0.2 L

Features

- Translation
- BMI calculation
- Weather reporting
- Tauri server status check

TRANSLATION (engine provided by yandex)
Translates a text from the source language to the target language. If no source language is preset, the translator will try to automatically detect it. The quality of the translations do not reflect the quality of the bot, and any mistaken translations are the exclusive responsibility of Yandex.
	Usage:
		>!ytr [source] [target] [text]
		>!ytr 	hu	en	labda
		>> ball
		#Automatic source detection
		>!ytr en labda
		>> ball
Engine by Google:
	Usage:
		>!gtr [source(optional)] [target] [text]

BMI calculation
Calculates the user's body mass index
	Usage:
		>!bmi [height] [weight]
		>!bmi 	175	70
		>!bmim 175		#Returns the ideal weight range for the user

Weather reporting
Returns the basic weather data for a given location (Temperature, sky conditions, humidity, air pressure, wind speed and direction) This service uses the OpenWeatherMap API. The bot is not responsible for any erroneous data supported by the third party service.
	Usage:
		>!weather London #Returns the weather of London

Tauri Server Status Check
Returns the status of the Tauri realm (online/offline)
	Usage:
		>!van-e Tauri
		>> Nincs
Allrealm check:
		>!szerverek
Returns the onnline/offline status and population of all realms in the xml

Tauri API
		>!am [character] [realm]
		>>Returns armory information of the given character on the given realm 

The full list of commands as well as a detailed description is available via the !chelp command

Legal notice
This IRC bot was developed by Daniel. All rights reserved. The code or parts of the code shall not be published without the permission of the developer. All API and module rights are held by their respective owner. The developer of this software cannot be held responsible for any misuse or malfunction of these modules. Furthermore, the developer does not guarantee that the modules not affiliated with the developer will provide sufficient level of service on a long term. The developer shall not be held liable for any misuse of the software.

For the GodX IRC channel, 2017-2018