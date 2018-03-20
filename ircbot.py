# -*- coding: utf-8 -*-
# - Add timestamps and timers should watch delta-time upon pinging instead of wait() == 30%
#TODO: Implement retorts for curses
#TODO: Order 66
#TODO: Codered?
#TODO: Administrative functions
#TODO: Better GetMSG with *args
#TODO: Check if today is a holiday at midnight (i. e. Xmas greetings)
#TODO: GetKeyword (PRIVMSG, KICK, ETC)


'''
KICK Syntax
[11:27:43] :NAME!IDENT@HOST KICK CHAN BOTNICK :REASON
'''

# Import some necessary libraries.
import pdb
import socket
import sys
import importlib
import serverinfo_module
import weather_module
import translator_module
import wow_leveling_module
import wikipedia_module
import bmi_module
import geo_module
from time import sleep as wait
import datetime
import os
from random import randint as roll
import gtranslate
import tauri_api
import traceback

#IRC_CODES                                  SYNTAX
CODE_READY          = '001'
CODE_AUTHED         = '307'
CODE_WHOIS1         = '311'
CODE_WHOIS_END      = '318'
CODE_TOPIC          = '332'                #[CODE] [BOTNICK] [CHAN] :[TOPIC]
CODE_TOPIC_SETBY    = '333'                #[CODE] [BOTNICK] [CHAN] [SETBY] [DATE]
CODE_NAMES          = '353'
CODE_NICK_TAKEN     = '433'                #Handling solved
CODE_NICKCHANGE_THROTTLED = '438'          #Handling needs to be solved
CODE_JOIN_THROTTLED = '500'                #Handling needs to be solved

class ForceQuit(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

# Some basic variables used to configure the bot
debug = False
owner = 'Daniel'
version = "I am a utility IRC Bot developed by Daniel in Python3. Born on 26 January 2017, last updated on 16 March 2018. Dedicated to the GodX channel." 
modules = ('serverinfo_module', 'weather_module', 'translator_module', 'tauri_api', 'wow_leveling_module', 'wikipedia_module', 'bmi_module', 'grammar', 'geo_module', 'gtranslate')
powerkickers = ('balintx', 'Chris', 'Higi', 'Crawen', 'Mokeszli', 'TauriBOT', 'Pompyro', 'Aithne', 'Jackcarver')
recovery_pass = 'correct horse battery staple'
protect = True
antiflood = 0
ignorelist = []
real = 0
on = True
commands = ('!chelp', '!weatherreport', '!forecast', '!distance', '!am', '!dt', "!sz", '!identify', '!additem', '!char', '!nextsun', '!nextclear', '!nextstorm', '!rain?', '!mibloc', '!isup', '!delitem', '!pickpocket', '!do', '!ab', '!page', '!noco', '!sh', '!str2time', '!dtr', '!wr', '!defuse', '!gtr', '!nextrain', '!timebomb', '!fc', '!pofon', '!nextsnow', '!gaspar', '!van-e', '!debug', '!part', '!joccak', '!chjoin', '!ytr', '!weather', '!leveling', '!reload', '!protect', '!map', '!wiki', '!af', '!szerverek', '!say', '!act', '!slap', '!setnick', '!bmi', '!bmim', '!ignore', '!unignore', '!ignorelist')
hasBomb = False
defuseNeeded = False
IsOwnerOnMainChannel = True #Ha ez nem vált vissza a megfelelő pillanatban, nagyon el tud baszódni minden
nocommentfile = '/ircbot/testrepo/noco.txt' #Linux-only, unused atm
itemfile = '/ircbot/testrepo/items.txt'
validName = False

if debug == False:
  choice = int(input('Hová szeretnél csatlakozni?\n0) Freenode\n1) Balintnet\n2) Tauri\n'))
  real = choice  

if real == 0:         # Freenode
  server = "chat.freenode.net"
  channel = "#danieltest"
  botnick = "Felix"
  realname = 'Wise men\'s child'
 
if real == 1:         # Balintnet
  server = 'irc.godx.pw'
  channel = '#phoenixchat'
  botnick = 'Marci'
  realname = 'Wise men\'s child'

if real == 2:          # 3rael5me
  server = 'irc.tauri.hu'
  channel = '#godx'
  botnick = 'Felix'
  realname = 'Not the bot you\'re looking for'
 
#Owner check
def CheckUserPrivilege():
  sender = GetSender()
  if (sender == owner and CheckUserAuth(sender) == True) or real == 0:
    return True
  else:
    return False

def IRC_COMM(typ, whom='', what=''):
  ircsock.send(bytes(("%s %s :%s\n" % (typ, whom, what)), 'utf-8')) 
  #print('%s, %s, %s' % (typ, whom, what))

#Újfajta pingelés
def ping2(msg):
  msg = str(msg).split(':')[1]
  ircsock.send(bytes("PONG :"+msg+"\n", 'utf-8'))

def sendmsg(chan, msg): # This is the send message function, it simply sends messages to the channel.
  IRC_COMM('PRIVMSG', chan, msg)

def sendact(chan, act):
  IRC_COMM('PRIVMSG', chan, '\x01ACTION '+act+'\x01')

def sendpm(user, msg):
  IRC_COMM('PRIVMSG', user, msg)
  #đprint('%s %s' % (user, msg))

def joinchan(chan): # This function is used to join channels.
  IRC_COMM('JOIN', chan)

def partactual(chan): #Parts basic channel
  IRC_COMM('PART', chan)

def kick(chan, whom):
  IRC_COMM('KICK', chan, whom) #NEEDS TESTING

def setnick(nick):
  global botnick
  botnick = nick
  IRC_COMM('NICK', nick)

def CheckCommandValidity(subject, command): #0.2 óta nem kell aposztrof a commandok után | 0.2.1 óta csak ircmsg után kell használni, command után nem. Ez alapból arra jó, hogy ha string közepén van a command, ne fusson le.
  box = str(subject).split(command)
  if len(box) != 1:
    return True
  else:
    return False

def GetMibIdent(nick): #ONLY USE ON MIBS
  ircsock.send(bytes("WHOIS :"+nick+"\n", 'utf-8'))
  ircmsg2 = ircsock.recv(1024)
  ircmsg2 = ircmsg2.strip(bytes('\n\r', 'utf-8'))
  ircmsg2 = ircmsg2.decode('utf-8', errors='ignore')
  if ircmsg2.find(CODE_WHOIS1) != -1:
    line = ircmsg2
  line = line.split(nick)[1].split()[0]
  return line

def CheckUserAuth(user):         #Ebben olyan kurva sok buktató lehet...
  ircsock.send(bytes("WHOIS :"+user+"\n", 'utf-8'))
  end = False
  while end == False:
    ircmsg2 = ircsock.recv(1024)
    ircmsg2 = ircmsg2.strip(bytes('\n\r', 'utf-8'))
    ircmsg2 = ircmsg2.decode('utf-8', errors='ignore')
    if ircmsg2.find(CODE_AUTHED) != -1:
      end = True
      return True
    if ircmsg2.find(CODE_WHOIS_END) != -1:
      end = True
      return False
  
def Hex2IP(hexip):
  if len(hexip) == 8:
    part1 = hexip[:2]
    part2 = hexip[2:4]
    part3 = hexip[4:6]
    part4 = hexip[6:8]
    part1 = int(part1, 16)
    part2 = int(part2, 16)
    part3 = int(part3, 16)
    part4 = int(part4, 16) #TODO: Rework into a loop
    ip = '%d.%d.%d.%d' % (part1, part2, part3, part4)
    return ip

def IsUserOnChannel(channel, user):
  channel = channel.lstrip('#')
  IRC_COMM('NAMES', "#"+channel)
  #userlist = []
  ircmsg2 = ircsock.recv(1024)
  ircmsg2 = ircmsg2.strip(bytes('\n\r', 'utf-8'))
  ircmsg2 = ircmsg2.decode('utf-8', errors='ignore')
  #if ircmsg.find(CODE_NAMES) == -1:
  #  while ircmsg.find(CODE_NAMES) == -1:                    #Valószínűleg felesleges, és biztosan unsafe
  #    ircmsg2 = ircsock.recv(1024)
  #    ircmsg2 = ircmsg2.strip(bytes('\n\r', 'utf-8'))
  #    ircmsg2 = ircmsg2.decode('utf-8', errors='ignore')   
  box = ircmsg2.split(':')[2]
  userlist = box.split()
  for i in range(len(userlist)):
    userlist[i] = userlist[i].lstrip('~&@%+')
    userlist[i] = userlist[i].lower()
  #print('USERS:'+str(userlist))
  if user.lower() in userlist:
    return True
  else:
    return False

def SendConsoleMessage(msg): #Timestamp-formatting
  #time = datetime.time()
  now = datetime.datetime.now().strftime('%H:%M:%S')
  try:
    print('[%s] %s' % (now, msg))
  except:
    print('Nem tudtam megjeleníteni egy messaget')

def GetCommand():
  chan = GetChannel()
  t = str(ircmsg).split(chan)
  box = t[1].split()
  try:
    command = box[0]
    commnad = command.strip("'")
    command = command.strip(':')
    command = command.lower()
    if command[0] == '!':
      sender = GetSender()
      for i in range(len(ignorelist)): #Ignore check
        if ignorelist[i] == sender and sender != owner and real > 0:
          return 'Ignored'
      return command
    else:
      pass
  #Ignore check
  except:
    SendConsoleMessage('Exception a GetCommand()-ban')

def GetSender():
  sender = ircmsg.split()[0].split('!')[0].strip(':')
  return sender

def GetMSG():                         #Obsolete
  msg = str(ircmsg.split(':', 2)[2])
  return msg

def GetBetterKickData(msg): #[11:27:43] :NAME!IDENT@HOST KICK CHAN BOTNICK :REASON
  kickedby = msg.split('!')[0].lstrip(':')
  kickedfrom = str(str(msg).split('KICK')[1]).split(':')[0].strip().split()[0]
  kickeduser = str(str(msg).split('KICK')[1]).split(':')[0].strip().split()[1]
  reason = str(msg).split(':')[2]
  return kickedby, kickedfrom, kickeduser, reason

def GetNewNick():
  t = ircmsg.split('NICK')
  newnick = t[1]
  newnick = newnick.strip(' ')
  newnick = newnick.strip(':')
  return newnick

def GetChannel():
  if ircmsg.find('PRIVMSG') != -1:
    t = str(ircmsg).split('PRIVMSG')
  elif ircmsg.find('KICK') != -1:
    t = str(ircmsg).split('KICK')
  elif ircmsg.find('INVITE') != -1:
    t = str(ircmsg).split('INVITE')[1].split()[1].lstrip()
    return t[1]
  chan = str(t[1]).split(':')[0].strip()
  return chan

def GetArgs(): # EGYTŐL_KEZDŐDIK_AZ_INDEXELÉS!!!!!!!
  chan = GetChannel()
  box = str(ircmsg).split(chan)[1].split(' ')[1:]
  return box

def SetMode(mode):
  IRC_COMM('MODE', botnick, '+%s' % mode)

def UnsetMode(mode):
  IRC_COMM('MODE', botnick, '-%s' % mode)

def SetChannelMode(channel, mode):
  IRC_COMM('MODE', channel, '+%s' % mode)

def UnsetChannelMode(channel, mode):
  IRC_COMM('MODE', channel, '-%s' % mode)

def Autorejoin():
  try:
    kickedby, kickedfrom, kickeduser, reason = GetBetterKickData(ircmsg)
    if kickedby not in powerkickers and kickeduser == botnick: #TODO: Saját nick tracking valamiért szar
      chan = GetChannel()
      joinchan(chan)
    if kickedby in powerkickers and reason.find('magad') != -1:
      chan = GetChannel()
      joinchan(chan)
  except:
    chan = GetChannel()
    joinchan(chan)
    sendmsg(chan, 'Exception in autorejoin')

def Ignore(target):
  onList = False
  for i in range(len(ignorelist)):
    if ignorelist[i] == target:
      onList = True
  if onList == False:
    ignorelist.append(target)

def Unignore(target):
  for i in range(len(ignorelist)):
    if ignorelist[i] == target:
      del ignorelist[i]

def Convert2byte(string):
  string = bytes(string, 'utf-8')
  return string

def SendInitDataToServer(nick, realname):
  ircsock.send(bytes("NICK "+ nick +"\n", 'utf-8')) # here we actually assign the nick to the bot
  ircsock.send(bytes("USER "+ nick +" "+ nick +" "+ nick +" : "+realname+"\n", 'utf-8')) # user authentication
  ircsock.send(bytes("NICK "+ nick +"\n", 'utf-8')) # here we actually assign the nick to the bot again because it likes to mess up
  if real != 1:
    wait(5)

#def Defuse():
#  box = ircmsg.split('bukkansz:')
#  colours = box[1].split()
#  target = roll(0, len(colours)-1)
#  for i in range(len(colours)):
#    colours[i] = ''.join(filter(lambda x: x.isalpha(), colours[i]))
#  chan = GetChannel()
#  sendmsg(chan, '!cutwire %s' % str(colours[target]))
#-----------------------------------[Connect]----------------------------------------------------     
assert real < 3             
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircmsg = ircsock.recv(2048) # receive data from the server
ircmsg = ircmsg.strip(bytes('\n\r', 'utf-8')) # removing any unnecessary linebreaks.
SendConsoleMessage(ircmsg) #Live feed

if ircmsg.find(bytes("PING :", 'utf-8')) != -1:
  ping2(ircmsg)

SendInitDataToServer(botnick, realname)

if ircmsg.find(bytes("PING :", 'utf-8')) != -1: # 2x kell pingelni néhány szerveren
  ping2(ircmsg)

#-----------------------------------[Commands]---------------------------------------------------------

while on == True: # Lehetőleg ne csináljunk deadloopot
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip(bytes('\n\r', 'utf-8')) # removing any unnecessary linebreaks.
  ircmsg = ircmsg.decode('utf-8', errors='ignore')
  command = ircmsg.lower()
  try:
    command = GetCommand()
  except:
  #  SendConsoleMessage('Command error.') #Ez valószínűleg nem error, csak nem erre számít (pl. pingelésnél). Ezért hagyjuk meg egyelőre a command-ircmsg dualitást. Persze igazán szép az volna, ha először megnézné, hogy command-e, és ha igen, nem kezelné ircmsgként is, de hát kinek van türelme ilyeneket megírni...
    pass #UPDATE: Meg lett már írva, de ez mégis failsafe megoldás, úgyhogy maradjon egyelőre (bele kéne nyúlni az if-elif-else dolgokba, és hát kinek van erre ideje...)

  if(ircmsg):
    SendConsoleMessage(ircmsg) #Kiír dolgokat a konzolba

  if IsOwnerOnMainChannel == False:   #Broadcastolja a main channel történéseit pm-ben az ownernek amíg nem rejoinol.
    try:
      chan = GetChannel()
      if chan == channel:
        sender = GetSender()
        msg = GetMSG()
        now = datetime.datetime.now().strftime('%H:%M:%S')
        sendpm(owner, '[%s] <%s>: %s' % (now, sender, msg))
        #print('(%s) [%s] <%s>: %s' % (owner, now, sender, msg))
    except:
      pass

  if ircmsg.find("001") != -1: #Ha 001 előtt akarsz bemenni, le fog dobni
      validName = True
      joinchan(channel) # Init after registration
      SetMode('Bx') #Bot flag & IP hide

  if ircmsg.find(CODE_NICK_TAKEN) and validName == False:
    botnick = botnick+'_'
    setnick(botnick)
    wait(5)

  if ircmsg.find("PING :") != -1:
    antiflood = 0
    ping2(ircmsg)

  if ircmsg.find('KICK #') != -1 and ircmsg.find('PRIVMSG') == -1:
    kickedby, kickedfrom, kickeduser, reason = GetBetterKickData(ircmsg)
    if kickeduser == owner and kickedfrom == channel:
      IsOwnerOnMainChannel = False
    elif kickeduser == botnick:
      Autorejoin()

  if ircmsg.find('JOIN') != -1:
    sender = GetSender()
    if sender == owner:
      IsOwnerOnMainChannel = True

  if ircmsg.find('NICK :') != -1:
    oldnick = GetSender()
    newnick = GetNewNick()
    if oldnick == owner:
      owner = newnick
      SendConsoleMessage('Debug: Az új owner: '+owner)
    for i in range(len(ignorelist)):
      if ignorelist[i] == oldnick:
        ignorelist[i] = newnick

  if command in commands:
    if debug == False and command != '!joccak':
      try:
        ExecuteCommand(command)
      except BaseException as e:
        chan = GetChannel()
        sendmsg(chan, 'Hiba történt a %s parancs végrehajtásakor: %s.' % (command, e)) #TODO: Írja ki az exception típusát is
        traceback.print_exc()
      finally:
        SendConsoleMessage('[COMMAND] Executed command: %s' % command)
    else:
      ExecuteCommand(command)

  def ExecuteCommand(command):
    chan = GetChannel()
    sender = GetSender()
    args = GetArgs()
    global antiflood

    if command == '!joccak' and CheckUserPrivilege() == True: #Terminate application
      IRC_COMM('QUIT', 'joccak')
      on = False
      wait(1)
      sys.exit()

    if command == '!part' and CheckUserPrivilege() == True : #Part channel TODO: Fogadjon el paramétert
      partactual(chan)

  #Serverinfo
    elif command == '!van-e': #xD
      serverinfo_response1, serverinfo_response2 = serverinfo_module.GetServerDetails(args[1])
      sendmsg(chan, serverinfo_response1)
      sendmsg(chan, serverinfo_response2)

    elif command == '!gtr':
      try:
        source = args[1]
        target = args[2]
        text = ''
        for i in range(3, len(args)):
          text += args[i] + ' '
        result = str(gtranslate.Translate(source, target, text))
        sendmsg(chan, result)
        wait(1) #Hogy ki ne banoljon a googleapi
      except Exception as e:
        sendmsg(chan, 'Hiba.')
        SendConsoleMessage('Caught an exception '+str(e))

    if command == '!identify':
      del args[0]
      text = str(args)
      #print(args)
      result = gtranslate.Detect(text)
      sendmsg(chan, result)
  
  #Translator
    elif command == '!ytr':
      try:
        source = args[1]
        target = args[2]
        text = ''
        for i in range(3, len(args)):
          text += args[i] + ' '
        #------[DEBUG]---------
        #SendConsoleMessage('Text: '+text)               #N.B.: CSAK DEBUGOLÁSRA! Ha ezek benne vannak a kódban, a cmd az encodingja miatt elég sok nyelvre crashelni fog.
        #SendConsoleMessage('Target: '+target)
        #SendConsoleMessage('Source: '+source)
        #------[/Debug]--------
        result = str(translator_module.Translate(text, target, source))
        sendmsg(chan, result)
      except Exception as e:
        sendmsg(chan, 'Helyes szintaxis: !ytr [forrásnyelv] [célnyelv] [szöveg]')
        SendConsoleMessage('Caught an exception '+str(e))

    elif command == '!dtr':
      try:
        src = args[1]
        tar = args[2]
        txt = ''
        for i in range(3, len(args)):
          txt += args[i] + ' '
        result = translator_module.DoubleTranslate(src, tar, txt)
        sendmsg(chan, result)
      except Exception as e:
        sendmsg(chan, 'Helytelen szintaxis.')
        SendConsoleMessage('Exception a !dtr-ben')

  #WoW Leveling Guide
    elif command == '!leveling':
      level = args[1]
      zone = wow_leveling_module.GetZone(level)
      sendmsg(chan, zone)

  #Channel Join
    elif command == '!chjoin' and CheckUserPrivilege() == True:
      target = args[1].lstrip()
      joinchan('#'+target)

  #Reloading modules
    elif command == '!reload' and CheckUserPrivilege() == True:
      target = args[1]
      chan = GetChannel()
      if target in modules:
        try:
          importlib.reload(sys.modules[target])
          sendmsg(chan, 'Modul újratöltve.')
        except:
          sendmsg(chan, 'Hiba történt, újratöltés megszakítva. Lehet, hogy a modul újraindításig nem fog megfelelően működni.')
      else:
        sendmsg(chan, 'Nincs ilyen modul.')

  #Timebomb protection ki-be kapcsoló
    elif command == '!protect' and CheckUserPrivilege() == True:
      global protect
      if protect == False:
        protect = True
        SendConsoleMessage('Védelem bekapcsolva')
      else:
        protect = False
        SendConsoleMessage('Védelem kikapcsolva')

    elif command == '!page':
      title = serverinfo_module.GetPageTitle(args[1])
      sendmsg(chan, title)

  #Ábel
    #if ircmsg.find("de miért?") != -1:
    #  chan = GetChannel()
    #  sendmsg(chan, 'http://i.imgur.com/UjbyV0T.jpg')

  #Medzsik
  #  if ircmsg.find("magic") != -1:
  #    chan = GetChannel()
  #    sendmsg(chan, 'http://i.imgur.com/eVxzDzy.gif')

  #Verekedős module
    elif command == '!pofon' and antiflood < 5 and protect == True:
      if chan == '#godx' or chan == '#phoenixchat' or real == 0:
        target = args[1]
        sender = GetSender()
        if target == owner:
          sendact(chan, 'megbosszulja Danielt')
          sendmsg(chan, '!pofon '+sender)
        elif target == botnick and sender != owner:
          sendmsg(chan, 'Anyádat')
          sendmsg(chan, '!pofon '+sender)
        antiflood += 1

    #Slap
    elif command == '!slap' and CheckUserPrivilege() == True:
      target = args[1]
      if target:
        sendact(chan, 'slaps '+target+' around a bit with a large trout')

    #Say
    elif command == '!say' and CheckUserPrivilege() == True:
      chan = args[1]
      if type(chan) == str:
        chan = '#'+chan
        text = ''
        for i in range(2, len(args)):
          text += args[i] + ' '
        if type(text) == str:
          sendmsg(chan, text)

    elif command == '!act' and CheckUserPrivilege() == True:
      chan = args[1]
      if type(chan) == str:
        chan = '#'+chan
        text = ''
        for i in range(2, len(args)):
          text += args[i] + ' '
        if type(text) == str:
          sendact(chan, text)
   
    #Nick átállítás
    elif command == '!setnick' and CheckUserPrivilege() == True:
      if type(args[1]) == str:
        setnick(args[1])

    #Commandhelp
    elif command == '!chelp':
      if len(args) > 1:
        arg = args[1]
        if arg.lower() == 'part':
          sendmsg(chan, 'Eltávolítja a botot a csatornáról.')
        elif arg.lower() == 'joccak':
          sendmsg(chan, 'Kikapcsolja a botot.')
        elif arg.lower() == 'van-e':
          sendmsg(chan, 'Megmutatja, online-e a Tauri/WoD, és hány ember van fenn. Használat: !van-e [Tauri/WoD]')
        elif arg.lower() == 'weather':
          sendmsg(chan, 'Megmutatja az időjárást egy adott helyen. Használat: !weather [városnév]')
        elif arg.lower() == 'ytr':
          sendmsg(chan, 'Minőségi fordítórendszer a Yandex jóvoltából. Használat: !ytr [forrásnyelv (opcionális)] [célnyelv] [szöveg]')
        elif arg.lower() == 'leveling':
          sendmsg(chan, 'Megmutatja, hogy egy adott szinten hol érdemes fejlődnöd. Használat: !leveling [level]')
        elif arg.lower() == 'chjoin':
          sendmsg(chan, 'Joinol a megadott csatornára. Használat: !chjoin [channel]')
        elif arg.lower() == 'reload':
          sendmsg(chan, 'Újratölti az adott modult. Használat: !reload [serverinfo_module/weather_module/wow_leveling_module/translator_module]')
        elif arg.lower() == 'protect':
          sendmsg(chan, 'Ki/bekapcsolja a timebomb és pofon védelmet.')
        elif arg.lower() == 'map':
          sendmsg(chan, 'Megkeres egy helyet a Google térképen. Használat: !map [helységnév]')
        elif arg.lower() == 'wiki':
          sendmsg(chan, 'Megkeres egy adott szócikket a wikipedián. Használat: !wiki [nyelv (opcionális)] [szócikk neve]')
        elif arg.lower() == 'af':
          sendmsg(chan, 'Reseteli az anti-floodot.')
        elif arg.lower() == 'szerverek':
          sendmsg(chan, 'Kilistázza a szerverek státuszát.')
        elif arg.lower() == 'say':
          sendmsg(chan, 'Mond valamit az adott channelen. Használat: !say [channel] [szöveg]')
        elif arg.lower() == 'act':
          sendmsg(chan, 'Csinál valamit a channelen. Használat: !act [channel] [szöveg]')
        elif arg.lower() == 'slap':
          sendmsg(chan, 'Megpofozza a targetet.')
        elif arg.lower() == 'setnick':
          sendmsg(chan, 'Átállítja a bot nickjét.')
        elif arg.lower() == 'bmi':
          sendmsg(chan, 'Kiszámolja a BMI-d. Használat: !bmi [magasság] [súly]')
        elif arg.lower() == 'bmim':
          sendmsg(chan, 'Kiszámolja az ideális súlyodat a magasságodhoz viszonyítva. Használat: !bmim [magasság]')
        elif arg.lower() == 'ignore':
          sendmsg(chan, 'Ignorál valakit. Használat: !ignore [kit]')
        elif arg.lower() == 'ignorelist':
          sendmsg(chan, 'Kiírja az ignorelistát')
        elif arg.lower() == 'unignore':
          sendmsg(chan, 'Leveszi az ignore-t az emberről. Használat: !unignore [kit]')
        elif arg.lower() == 'wr' or arg.lower() == 'weatherreport':
          sendmsg(chan, 'Kiírja az adott település időjárását. Ha nincs település megadva, az alap godxvárosokat írja ki.')
        elif arg.lower() == 'nextrain' or arg.lower() == 'nextsnow':
          sendmsg(chan, 'Kiírja, várható-e a következő 5 napban az adott csapadék')
        else:
          sendmsg(chan, 'Nincs ilyen parancs, vagy nincs súgó hozzá')
      else:
        x = ''
        for i in range(len(commands)):
          x += commands[i] + ' '
        sendmsg(chan, 'Parancsok: '+ x)

      #Google térkép
    elif command == '!map':
      del(args[0])
      loc = ' '.join(args)
      link = geo_module.GetLocation(loc)
      sendmsg(chan, link)

      #Wikipedia kereső
    elif command == '!wiki':
      text = ''
      for i in range(len(args)):
        text += args[i]
      chan = GetChannel()
      if type(text) == str:
        result = wikipedia_module.Search(text)
        sendmsg(chan, result)

      #Allrealm info
    elif command == '!szerverek' or command == '!sz' and antiflood < 5:
      response = serverinfo_module.GetCollectiveDetails()
      sendmsg(chan, response)
      antiflood += 1

    elif command == '!bmi':
      if len(args) == 3:
        try:
          heigth = int(args[1])
          weigth = int(args[2])
        except:
          sendmsg(chan, 'Használat: !bmi [magasság] [testtömeg]')
        else:
          response = bmi_module.CalculateBMI(heigth, weigth)
          sendmsg(chan, response)
          antiflood += 1
      else:
        sendmsg(chan, 'Haszánlat: !bmi [magasság] [testtömeg]')

    elif command == '!defuse' and CheckUserPrivilege() == True:
      if len(args) == 2:
        sendact(chan, 'the Bomb Expert saves another soul.')
        sendmsg(chan, '!cutwire %s' % args[1])

    elif command == '!bmim':
      if len(args) == 2:
        chan = GetChannel()
        try:
          heigth = int(args[1])
        except:
          sendmsg(chan, 'Használat: !bmim [magasságod]')
        else:
          response = bmi_module.CalculateIdealWeight(heigth)
          sendmsg(chan, response)
          antiflood += 1
      else:
        sendmsg(chan, 'Használat: !bmim [magasságod]')

      #Manual Anti-flood reset
    elif command == '!af' and CheckUserPrivilege() == True:
      antiflood = 0
   
    elif command == '!ignore' and CheckUserPrivilege() == True:
      box = GetArgs()
      Ignore(box[1])
      sendmsg(chan, '%s ignorálva.' % box[1])

    elif command == '!ignorelist':
      x = ''
      for i in range(len(ignorelist)):
        x = '%s, ' % ignorelist[i]
      sendmsg(chan, x)

    elif command == '!unignore' and CheckUserPrivilege() == True:
      box = GetArgs()
      Unignore(box[1])
      sendmsg(chan, '%s unignorálva.' % box[1])

#=========================[Időjárás commandok]================================
    elif command == '!weatherreport' or command == '!wr' or command == '!weather' or command == '!fc' or command == '!forecast':
      if len(args) != 1:
        del(args[0])
        last = len(args)
        days = args[last-1]
        try:
          days = int(days)
        except:
          pass
        if type(days) == int:
          if days < 6:
            del(args[last-1])
            city = ' '.join(args)
            days = str(days)
            line = weather_module.GetForecast(city, days)   #t.i. args a város, last a napok száma, de lustaság van
            sendmsg(chan, line)
        elif days.find('hr') != -1 and days[0] in ['0', '1', '2', "3", '4', '5', '6', '7', '8', '9']:
          del(args[last-1])
          city = ' '.join(args)
          days = str(days)
          line = weather_module.GetForecast(city, days)   #t.i. args a város, last a napok száma, de lustaság van
          sendmsg(chan, line)
        else:
          args = ' '.join(args)
          line1, line2 = weather_module.GetWeatherData(args)
          sendmsg(chan, line1)
          sendmsg(chan, line2)
      else:
        response = weather_module.GetGodxUpdate()
        sendmsg(chan, response)

    #elif command == '!forecast' or command == '!fc':
    #  if len(args) >= 3: #Mert ugye van 0. csak nincs [ Command | Település [+Településnév2, etc.] | Időtartam ]
    #    del(args[0])
    #    city = ''
    #    for i in range(len(args)):
    #      if args[i] not in ('3hr', '1', '2', '3', '4', '5'):
    #        city += args[i] + ' '
    #      else:
    #        time = args[i]
    #    response = weather_module.GetForecast(city, time)
    #    sendmsg(chan, response)
    #  else:
    #      sendmsg(chan, 'Helytelen szintaxis. Használat: !forecast [helység] [napok száma | 3hr]')

    elif command == '!nextrain':
      if len(args) < 2:
        sendmsg(chan, 'Helytelen szintaxis. Használat: !nextrain [helység]')
      else:
        del(args[0])
        args = ' '.join(args)
        response = weather_module.GetNextRain(args)
        sendmsg(chan, response)

    elif command == '!nextsnow':
      if len(args) < 2:
        sendmsg(chan, 'Helytelen szintaxis. Használat: !nextsnow [helység]')
      else:
        del(args[0])
        args = ' '.join(args)
        response = weather_module.GetNextSnow(args)
        sendmsg(chan, response)

    elif command == '!nextsun' or command == '!nextclear':
      if len(args) < 2:
        sendmsg(chan, 'Helytelen szintaxis. Használat: !nextclear [helység]')
      else:
        del(args[0])
        args = ' '.join(args)
        response = weather_module.GetNextClear(args)
        sendmsg(chan, response)

    elif command == '!nextstorm':
      if len(args) < 2:
        sendmsg(chan, 'Helytelen szintaxis. Használat: !nextstorm [helység]')
      else:
        del(args[0])
        args = ' '.join(args)
        response = weather_module.GetNextStorm(args)
        sendmsg(chan, response)

    elif command == '!rain?':
      if len(args) < 3:
        sendmsg(chan, 'Helytelen szintaxis. Használat: !rain? [helység] [YYYY-MM-DD HH:MM]')
      else:
        del(args[0])
        #args = ' '.join(args)
        response = weather_module.CheckIfRain(args[0], args[1])
        sendmsg(chan, response)
#--------------------------------------------------------------------------------/weather
    elif command == '!debug' and CheckUserPrivilege() == True:
      global debug
      if debug == False:
        debug = True
        sendmsg(chan, 'Safe mode off')
      else:
        debug = False
        sendmsg(chan, 'Safe mode on')

    elif command == '!str2time':
      try:
        box = GetArgs()
        time = datetime.datetime.fromtimestamp(int(box[1]))
        sendmsg(chan, time.strftime('%Y-%m-%d %H:%M:%S'))
      except:
        SendConsoleMessage('Nem megy')

    elif command == '!mibloc':
      if len(args) > 1:
        #nick = args[1]
        #if nick.find("mib") != -1:
        #  ident = GetMibIdent(nick)
        #  print('++++++++++++!'+ident)
        #  ip = Hex2IP(ident)
        #  response = geo_module.GetIPLocation(ip)
        #  sendmsg(chan, response)
        CheckUserAuth(args[1])


    elif command == '!gaspar':
      load = str(os.getloadavg())
      with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(datetime.timedelta(seconds = uptime_seconds))
        uptime_string = uptime_string[:-7]
        load = load.strip('()')
      sendmsg(chan, 'Uptime: %s | Load: %s' % (uptime_string, load))

    elif command == '!distance' or command == '!dt':
      del(args[0])
      args = ' '.join(args)
      args = args.split('--')
      city1 = args[0]
      city2 = args[1]
      sendmsg(chan, geo_module.MeasureDistance(city1, city2))

    elif command == '!ab' and GetSender() == owner:
      global IsOwnerOnMainChannel
      if IsOwnerOnMainChannel == False:
        IsOwnerOnMainChannel = True
        print('Átváltva')
      elif IsOwnerOnMainChannel == True:
        IsOwnerOnMainChannel = False
        print('Visszaváltva')

    #if command == '!do':    #CSAK DEBUGRA!!!!!!!
    #  assert real == 0
    #  args = GetArgs()
    #  del(args[0])
    #  args = ' '.join(args)
    #  eval(args)


    #if command == '!noco':
    #  args = GetArgs()
    #  if len(args) == 1:
    #    chan = GetChannel()
    #    with open(nocommentfile, encoding='utf-8') as f:
    #      content = f.readlines()
    #      content = [x.strip() for x in content] 
    #      f.close()
    #    x = roll(0, len(content)-1) #-1 a tömb miatt és -1 az üres sor miatt
    #    sendmsg(chan, content[x])
    #  elif len(args) > 1:
    #    del(args[0])
    #    args = ' '.join(args)
    #    with open(nocommentfile, "a", encoding='utf-8') as f:
    #      f.write('%s\r\n' % args)
    #      f.close()

    elif command == '!additem':
      if len(args) < 2:
        pass
      else:
        del(args[0])
        args = ' '.join(args)
        #args += '\r\n'
        valid = True
        with open(itemfile, 'r', encoding='utf-8') as f:
          line = f.readline()
          line = line.strip()
          while line:
            if args == line:
              valid = False
              sendmsg(chan, 'Az item már a listában van.')
              break
            line = f.readline()
            line = line.strip()
          f.close()
        if valid == True:
          with open(itemfile, "a", encoding='utf-8') as f:
            f.write('%s\r\n' % args)
            f.close()
          sendmsg(chan, "Item hozzáadva")

    elif command == '!delitem': #Rework: Check az nagyon ocsmány
      if len(args) < 2:
        pass
      else:
        del(args[0])
        args = ' '.join(args)
        valid = False
        with open(itemfile, 'r', encoding='utf-8') as f:
          line = f.readline()
          line = line.strip()
          while line:
            if args == line:
              valid = True
              break
            line = f.readline()
            line = line.strip()
          f.close()
        if valid == True:
          with open(itemfile, 'r', encoding='utf-8') as f:
            content = f.readlines()
            f.close()
          with open(itemfile, 'w', encoding='utf-8') as f:
            for line in content:
              line = line.strip()
              if line != args:
                f.write(line+'\r\n')
            f.close()
            sendmsg(chan, 'Törölve.')
        else:
          sendmsg(chan, 'Nincs ilyen item a listában.')

    elif command == '!pickpocket' and real < 2:
      if len(args) > 1:
        target = args[1]
        if IsUserOnChannel(chan, target) == False:
          sendmsg(chan, '%s nincs a csatornán.' % target)
        else:
          with open(itemfile, encoding='utf-8') as f:
            content = f.readlines()
            content = [x.strip() for x in content] 
            f.close()
          x = roll(0, len(content)-1) #-1 a tömb miatt és -1 az üres sor miatt
          sendmsg(chan, "%s %s zsebébe nyúl, és ezt találja: %s" % (sender, target, content[x]))


    elif command == '!am':
      char = args[1]
      realm = args[2]
      result, link = tauri_api.GetCharacterData(char, realm)
      sendmsg(chan, result)
      sendmsg(chan, link)

    elif command == '!char':
      char = args[1]
      realm = args[2]
      link = tauri_api.GetLinkToCharacter(char, realm)
      sendmsg(chan, link)

    elif command == '!isup':
      site = args[1]
      code = serverinfo_module.GetResponseStatus(site)
      sendmsg(chan, code)


  #Shruggie
  if ircmsg.find(":x/sh") != -1 and CheckCommandValidity(ircmsg, ":x/sh") == True or command == '!sh':
    chan = GetChannel()
    sendmsg(chan, '¯\_(ツ)_/¯')

  #CTCP Version válasz
  if ircmsg.find(":\x01VERSION\x01") != -1: #TODO: Rework into a function
    sender = GetSender()
    IRC_COMM('NOTICE', sender, "\x01VERSION "+version+"\x01\n")

  if ircmsg.find(":\x01PING") != -1:
    sender = GetSender()
    args = GetArgs()
    pg = args[1]
    pg = pg[:-1]
    print(pg)
    IRC_COMM('NOTICE', sender, "\x01PING "+pg+'\x01\n')

#  if command == '!timebomb' and protect == True:
#    args = GetArgs()
#    try:
#      target = args[1]
#      chan = GetChannel()
#      if target == owner and chan in ('#godx', '#phoenixchat', '#danieltest'):
#        hasBomb = True
#    except:
#      pass
#
#  if ircmsg.find("erősített %s testéhez" % owner) != -1 and hasBomb == True:
#    defuseNeeded = True
#
#  if ircmsg.find("vezetékre bukkansz:") != -1 and protect == True and hasBomb == True and defuseNeeded == True:
#    hasBomb = False
#    defuseNeeded = False
#    sendact(chan, 'megpróbálja megmenteni %s életét' % owner)
#    Defuse()

  #Recovery
  if ircmsg.find(recovery_pass) != -1:
    chan = GetChannel()
    chan = chan.strip('#')
    if chan == botnick:
      sender = GetSender()
      owner = sender
      sendmsg(sender, 'Recovery successful')
      SendConsoleMessage('Owner changed to: '+owner)

  if ircmsg.find('INVITE') != -1:
    chan = GetChannel()
    joinchan(chan)

  #Join-throttling UNTESTED!
  if ircmsg.find('Too many join requests') != -1 and ircmsg.find(CODE_JOIN_THROTTLED) != -1:
    SendConsoleMessage('DEBUG: Too many join requests message received. Waiting for 5 minutes before trying to rejoin again.')
    chan = GetChannel()
    wait(300)
    joinchan(chan)