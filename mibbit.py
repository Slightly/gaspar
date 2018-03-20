import socket
import datetime
import sys
from time import sleep as wait
import geo_module

CODE_READY = '001'
CODE_WHOIS1 = '311'

owner = 'Daniel'
version = "Mibbit locator by Daniel" 
recovery_pass = 'changeme'
server = 'irc.tauri.hu'
channel = '#wow'
botnick = 'asd'
realname = 'nemvapid'
on = True
bchan = '#mib'

commands = ('!joccak', '!asd')

def IRC_COMM(typ, whom='', what=''):
  ircsock.send(bytes(("%s %s :%s\n" % (typ, whom, what)), 'utf-8')) 

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

def SendConsoleMessage(msg): #Timestamp-formatting
 #time = datetime.time()
 now = datetime.datetime.now().strftime('%H:%M:%S')
 print('[%s] %s' % (now, msg))

def SetMode(mode):
  IRC_COMM('MODE', botnick, '+%s' % mode)

def GetSender():
 sender = ircmsg.split()[0].split('!')[0].strip(':')
 return sender

def CheckUserPrivilege():
 sender = GetSender()
 if sender == owner or real == 0:
   return True
 else:
   return False

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
      return command
    else:
      pass
  #Ignore check
  except:
    SendConsoleMessage('Exception a GetCommand()-ban')

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

def GetMibIdent(nick): #ONLY USE ON MIBS
  ircsock.send(bytes("WHOIS :"+nick+"\n", 'utf-8'))
  ircmsg2 = ircsock.recv(1024)
  ircmsg2 = ircmsg2.strip(bytes('\n\r', 'utf-8'))
  ircmsg2 = ircmsg2.decode('utf-8', errors='ignore')
  if ircmsg2.find(CODE_WHOIS1) != -1:
    line = ircmsg2
  line = line.split(nick)[1].split()[0]
  return line

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircmsg = ircsock.recv(2048) # receive data from the server
ircmsg = ircmsg.strip(bytes('\n\r', 'utf-8')) # removing any unnecessary linebreaks.
SendConsoleMessage(ircmsg) #Live feed

if ircmsg.find(bytes("PING :", 'utf-8')) != -1:
  ping2(ircmsg)

ircsock.send(bytes("NICK "+ botnick +"\n", 'utf-8')) # here we actually assign the nick to the bot
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" : "+realname+"\n", 'utf-8')) # user authentication
ircsock.send(bytes("NICK "+ botnick +"\n", 'utf-8')) # here we actually assign the nick to the bot again because it likes to mess up

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
  #  SendConsoleMessage('Command error.') 
    pass

  try:
    SendConsoleMessage(ircmsg) #Kiír dolgokat a konzolba
  except:
    SendConsoleMessage('Nem tudtam megjeleníteni egy ircmsg-t.')

  if ircmsg.find(CODE_READY) != -1: #Ha 001 előtt akarsz bemenni, le fog dobni
      joinchan(channel) # Init after registration
      joinchan(bchan)
      SetMode('Bx') #Bot flag & IP hide

  if ircmsg.find("PING :") != -1:
    ping2(ircmsg)

  if ircmsg.find('NICK :') != -1:
    oldnick = GetSender()
    newnick = GetNewNick()
    if oldnick == owner:
      owner = newnick
      #SendConsoleMessage('Debug: Az új owner: '+owner)

  if command in commands:
    try:
   	  ExecuteCommand(command)
    except BaseException as e:
      if command == '!joccak' and CheckUserPrivilege() == True:
      	ExecuteCommand(command)
      else:
        chan = GetChannel()
        sendmsg(bchan, 'Hiba történt a %s parancs végrehajtásakor: %s.' % (command, e)) #TODO: Írja ki az exception típusát is
    finally:
      SendConsoleMessage('[COMMAND] Handled command: %s' % command)

  def ExecuteCommand(command):
    if command == '!joccak' and CheckUserPrivilege() == True: #Terminate application
      on = False
      sys.exit()

  if ircmsg.find(recovery_pass) != -1:
    chan = GetChannel()
    chan = chan.strip('#')
    if chan == botnick:
      sender = GetSender()
      owner = sender
      sendmsg(sender, 'Recovery successful')
      SendConsoleMessage('Owner changed to: '+owner)

  if ircmsg.find('JOIN') != -1:
    if ircmsg.find('mibbit') != -1:
      nick = GetSender()
      ident = GetMibIdent(nick)
      ip = Hex2IP(ident)
      loc = geo_module.GetIPLocation(ip)
      response = "%s (%s) connected from %s" % (nick, ip, loc)
      sendmsg(bchan, response)
