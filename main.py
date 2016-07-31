# Version 3.1 - added security features
# !/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import json
import telepot
from threading import Timer
import os
from bs4 import BeautifulSoup
from mechanize import Browser
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot('insert_bot_token_here')

serverboolean = {}
inlinedata = {}
usersblocked = {}

# /start command

def start(msg):
	chat_id = msg['chat']['id']
	bot.sendChatAction(chat_id, 'typing')
	start_keyboard = {'keyboard':[[u"\U0001f4ca"+" Servers Stats",u"\u23f0"+" Game Time"],[u"\U0001f69a"+" "+u"\U0001f69a"+" Convoys List",u"\U0001f6e3"+" Kat_pw Stream Preview"],[u"\u2139\ufe0f"+" General Information"]]}
	bot.sendMessage(chat_id, "Welcome. Choose what you want to know "+u"\u2b07\ufe0f", reply_markup=start_keyboard )

# /restart command		

def restart(msg):
	global serverboolean
	chat_id = msg['chat']['id']
	serverboolean[chat_id] = False
	emo = u"\U0001f69a" + " "
	restart_keyboard = {'keyboard':[[u"\U0001f4ca"+" Servers Stats",u"\u23f0"+" Game Time"],[u"\U0001f69a"+" "+u"\U0001f69a"+" Convoys List",u"\U0001f6e3"+" Kat_pw Stream Preview"],[u"\u2139\ufe0f"+" General Information"]]}
	bot.sendMessage(chat_id, emo*6, reply_markup=restart_keyboard)

# Send a list of all available server

def serversstats(msg):
	chat_id = msg['chat']['id']
	text = msg['text']
	global serverboolean
	response = urllib.urlopen("http://api.truckersmp.com/v2/servers")
	html1 = response.read()
	html = json.loads(html1)
	poemi = html.get("response")
	inviareprimo = []
	for i in range(0,10):
		try:
			europe = u"\U0001f1ea\U0001f1fa"
			usa = u"\U0001f1fa\U0001f1f8"
			hongkong = u"\U0001f1ed\U0001f1f0"
			if "Europe" in poemi[i]["name"]:
				testodaimmettere = [europe + " " + str(poemi[i]["name"]) + " (" + str(poemi[i]["game"]) + ")"]
			elif "United States" in poemi[i]["name"]:
				testodaimmettere = [usa + " " + str(poemi[i]["name"]) + " (" + str(poemi[i]["game"]) + ")"]
			elif "Hong Kong" in poemi[i]["name"]:
				testodaimmettere = [hongkong + " " + str(poemi[i]["name"]) + " (" + str(poemi[i]["game"]) + ")"]
			else:
				testodaimmettere = [str(poemi[i]["name"]) + " (" + str(poemi[i]["game"]) + ")"]
			inviareprimo.append(testodaimmettere)
			i += 1
		except (KeyError,IndexError) as e:
			break
	server_keyboard = {'keyboard': inviareprimo }
	bot.sendMessage(chat_id, "Choose the server:", reply_markup=server_keyboard)
	serverboolean[chat_id] = True

# Send the stats of the chosen server

def serversstats1(msg):
	global serverboolean
	chat_id = msg['chat']['id']
	serverboolean[chat_id] = True
	bot.sendChatAction(chat_id, 'typing')
	text = msg['text']
	response = urllib.urlopen("http://api.truckersmp.com/v2/servers")
	html1 = response.read()
	html = json.loads(html1)
	poemi = html.get("response")
	i = None
	for i in range(0,10):
		searchitem = str(poemi[i]["name"]) + " (" + str(poemi[i]["game"]) + ")"
		if searchitem in text:
			break
		i += 1
	good = u"\u2705"
	bad = u"\u274c"
	remember = u"\u2757\ufe0f"
	restart_keyboard = {'keyboard':[[u"\U0001f4ca"+" Servers Stats",u"\u23f0"+" Game Time"],[u"\U0001f69a"+" "+u"\U0001f69a"+" Convoys List",u"\U0001f6e3"+" Kat_pw Stream Preview"],[u"\u2139\ufe0f"+" General Information"]]}
	error = html.get("error")
	if error == "false":
		message = "<b>Status of the server "+searchitem+"\n</b>"
		if html["response"][i]["online"] == True:
			message += good+" Server is online\n"
			message += "There are "+str(html["response"][i]["players"])+" players of "+str(html["response"][i]["maxplayers"])
			if html["response"][i]["speedlimiter"] == 1:
				message += "\n"+remember+" <b>Remember</b>: in this server there is the speed limiter of 110 km/h"
		else:
			message += bad+" Server is offline"
		bot.sendMessage(chat_id, message, parse_mode='Html', reply_markup=restart_keyboard)

# Send current game time

def gametime(msg):
	chat_id = msg['chat']['id']
	bot.sendChatAction(chat_id, 'typing')
	time = urllib.urlopen("http://api.truckersmp.com/v2/game_time")
	time1 = time.read()
	gametime1 = json.loads(time1)
	error = gametime1["error"]
	if error == False:
		time12 = gametime1["game_time"]
		message = "Time on servers of TruckersMP " + u"\u27a1\ufe0f" + " "
		mintot = time12 - 1
		settimanetot = mintot / 10080.00000000 
		settimanetot1 = int(settimanetot)
		settimanefinale = settimanetot - settimanetot1
		giornitot = settimanefinale*7.00000000 
		giornitot1 = int(giornitot)
		if giornitot1 == 0:
			message += "Monday"+" "
		elif giornitot1 == 1:
			message += "Tuesday"+" "
		elif giornitot1 == 2:
			message += "Wednesday"+" "
		elif giornitot1 == 3:
			message += "Thursday"+" "
		elif giornitot1 == 4:
			message += "Friday"+" "
		elif giornitot1 == 5:
			message += "Saturday"+" "
		elif giornitot1 == 6:
			message += "Sunday"+" "
		giornifinale = giornitot- giornitot1
		oretot = giornifinale*24.00000000 
		oretot1 = int(oretot)
		message += str(oretot1)+":"
		orefinale= oretot - oretot1
		minutitot= orefinale*60
		if int(minutitot) == 0 or int(minutitot) == 1 or int(minutitot) == 2 or int(minutitot) == 3 or int(minutitot) == 4 or int(minutitot) == 5 or int(minutitot) == 6 or int(minutitot) == 7 or int(minutitot) == 8 or int(minutitot) == 9:
			message += "0" + str(int(minutitot))
		else:
			message += str(int(minutitot))
		if oretot1 == 18 or oretot1 == 19 or oretot1 == 20 or oretot1 == 21 or oretot1 == 22 or oretot1 == 23 or oretot1 == 24 or oretot1 == 0 or oretot1 == 1 or oretot1 == 2 or oretot1 == 3 or oretot1 == 4 or oretot1 == 5 or oretot1 == 6:
			message += "\n"+u"\U0001f303"+" It's night so please *keep lights on* "+u"\U0001f4a1"
	else:
		message = "An error occurred."
	bot.sendMessage(chat_id, message , parse_mode='Markdown')

# If stream is online send a preview of the stream, else send a message

def gettwitch(msg):
	chat_id = msg['chat']['id']
	response = urllib.urlopen("https://api.twitch.tv/kraken/streams/kat_pw")
	response1 = response.read()
	response2 = json.loads(response1)
	if response2.get("stream") == None:
		bot.sendChatAction(chat_id, 'typing')
		bot.sendMessage(chat_id, u"\u26a0\ufe0f" +  " *Stream is offline now*", parse_mode="Markdown")
	else:
		bot.sendChatAction(chat_id, 'upload_photo')
		richiesta = response2.get("stream")
		richiesta1 = richiesta.get("preview")
		urllib.urlretrieve(richiesta1["large"], "preview.jpg")
		bot.sendPhoto(chat_id, open("preview.jpg") , caption="Here is the preview of the stream\nLink to stream -> https://www.twitch.tv/kat_pw")
		os.remove('preview.jpg')

# Send General information

def geninformation(msg):
	message = "Bot created by @EdoardoGrassiXYZ\n"
	message += u"\U0001f539" + "Bot version: 0.3.1 _alpha_\n"
	chat_id = msg["chat"]["id"]
	response = urllib.urlopen("https://api.truckersmp.com/v2/version")
	stringa = response.read()
	html = json.loads(stringa)
	message += u"\U0001f539" + "TruckersMP mod version: " + html.get("name") + " _" + html.get("stage") + "_ \n"
	message += u"\U0001f539" + "ETS2 version supported: " + html.get("supported_game_version") + "\n"
	message += u"\U0001f539" + "ATS version supported: " + html.get("supported_ats_game_version")
	bot.sendMessage(chat_id, message, parse_mode="Markdown")

# Send the first page of convoys list

def convoylist(msg):
	global inlinedata
	chat_id = msg['chat']['id']
	bot.sendChatAction(chat_id, 'typing')
	lista = urllib.urlopen("http://ets2c.com/")
	lista1 = lista.read()
	soup = BeautifulSoup(lista1, "lxml" )
	lista2 = soup.find_all("div", class_="row")[1:4]
	liste = []
	link1 = []
	for i in range(0,3):
		testopreso1 = lista2[i].getText()
		testopreso2 = testopreso1.replace("<","")
		testopreso = testopreso2.replace(">","")
		listaelaborata = testopreso.split("\n")
		liste.append(listaelaborata)
		i += 1
	for link in soup.find_all('a')[12:15]:
		link1.append(link.get('href'))
	basta = u"\U0001f537"
	message = u"\u2757\ufe0f" + " Upcoming Events " + u"\u2757\ufe0f" + "\n\n"
	message += basta + " Server: " + liste[0][1] + "\n  - Time: " + liste[0][2] + "\n  - Location: " + liste[0][3] + "\n  - Organiser: " + liste[0][4] + "\n  - Language: " + liste[0][5] + "\n  - Participants: " + liste[0][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[0] + u"\u0022" + " >More Info</a>"  + "\n\n"
	message += basta + " Server: " + liste[1][1] + "\n  - Time: " + liste[1][2] + "\n  - Location: " + liste[1][3] + "\n  - Organiser: " + liste[1][4] + "\n  - Language: " + liste[1][5] + "\n  - Participants: " + liste[1][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[1] + u"\u0022" + " >More Info</a>" + "\n\n"
	message += basta + " Server: " + liste[2][1] + "\n  - Time: " + liste[2][2] + "\n  - Location: " + liste[2][3] + "\n  - Organiser: " + liste[2][4] + "\n  - Language: " + liste[2][5] + "\n  - Participants: " + liste[2][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[2] + u"\u0022" + " >More Info</a>"
	t_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='< 1 >', callback_data='edit1'),InlineKeyboardButton(text=' 2 ', callback_data='edit2'),InlineKeyboardButton(text=' 3 ', callback_data='edit3'),InlineKeyboardButton(text=' 4 ', callback_data='edit4')]])
	sendedmessage = bot.sendMessage(chat_id,message,reply_markup=t_keyboard ,parse_mode='HTML')
	inlinedata[chat_id] = sendedmessage['message_id']

# Also this send the first page from convoys list, but work only if the user click on the button of the Inline Keyboard

def convoylist11(msg):
	chat_id21 = msg['from']['id']
	idsa = msg['id']
	data21 = msg['data']
	lista = urllib.urlopen("http://ets2c.com/")
	lista1 = lista.read()
	soup = BeautifulSoup(lista1, "lxml" )
	lista2 = soup.find_all("div", class_="row")[1:4]
	liste = []
	link1 = []
	for i in range(0,3):
		testopreso1 = lista2[i].getText()
		testopreso2 = testopreso1.replace("<","")
		testopreso = testopreso2.replace(">","")
		listaelaborata = testopreso.split("\n")
		liste.append(listaelaborata)
		i += 1
	for link in soup.find_all('a')[12:15]:
		link1.append(link.get('href'))
	basta = u"\U0001f537"
	message = u"\u2757\ufe0f" + " Upcoming Events " + u"\u2757\ufe0f" + "\n\n"
	message += basta + " Server: " + liste[0][1] + "\n  - Time: " + liste[0][2] + "\n  - Location: " + liste[0][3] + "\n  - Organiser: " + liste[0][4] + "\n  - Language: " + liste[0][5] + "\n  - Participants: " + liste[0][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[0] + u"\u0022" + " >More Info</a>"  + "\n\n"
	message += basta + " Server: " + liste[1][1] + "\n  - Time: " + liste[1][2] + "\n  - Location: " + liste[1][3] + "\n  - Organiser: " + liste[1][4] + "\n  - Language: " + liste[1][5] + "\n  - Participants: " + liste[1][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[1] + u"\u0022" + " >More Info</a>" + "\n\n"
	message += basta + " Server: " + liste[2][1] + "\n  - Time: " + liste[2][2] + "\n  - Location: " + liste[2][3] + "\n  - Organiser: " + liste[2][4] + "\n  - Language: " + liste[2][5] + "\n  - Participants: " + liste[2][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[2] + u"\u0022" + " >More Info</a>"
	msgid = (chat_id21, inlinedata.get(chat_id21))
	t_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='< 1 >', callback_data='edit1'),InlineKeyboardButton(text=' 2 ', callback_data='edit2'),InlineKeyboardButton(text=' 3 ', callback_data='edit3'),InlineKeyboardButton(text=' 4 ', callback_data='edit4')]])
	bot.editMessageText(msgid,message,reply_markup=t_keyboard ,parse_mode='HTML')
	bot.answerCallbackQuery(idsa, text='Convoys List Updated')

# Send the second page from convoys list

def convoylist1(msg):
	chat_id21 = msg['from']['id']
	idsa = msg['id']
	lista = urllib.urlopen("http://ets2c.com/")
	lista1 = lista.read()
	soup = BeautifulSoup(lista1, "lxml" )
	lista2 = soup.find_all("div", class_="row")[4:7]
	liste = []
	link1 = []
	for i in range(0,3):
		testopreso1 = lista2[i].getText()
		testopreso2 = testopreso1.replace("<","")
		testopreso = testopreso2.replace(">","")
		listaelaborata = testopreso.split("\n")
		liste.append(listaelaborata)
		i += 1
	for link in soup.find_all('a')[15:18]:
			link1.append(link.get('href'))
	basta = u"\U0001f537"
	message = u"\u2757\ufe0f" + " Upcoming Events " + u"\u2757\ufe0f" + "\n\n"
	message += basta + " Server: " + liste[0][1] + "\n  - Time: " + liste[0][2] + "\n  - Location: " + liste[0][3] + "\n  - Organiser: " + liste[0][4] + "\n  - Language: " + liste[0][5] + "\n  - Participants: " + liste[0][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[0] + u"\u0022" + " >More Info</a>"  + "\n\n"
	message += basta + " Server: " + liste[1][1] + "\n  - Time: " + liste[1][2] + "\n  - Location: " + liste[1][3] + "\n  - Organiser: " + liste[1][4] + "\n  - Language: " + liste[1][5] + "\n  - Participants: " + liste[1][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[1] + u"\u0022" + " >More Info</a>"  + "\n\n"
	message += basta + " Server: " + liste[2][1] + "\n  - Time: " + liste[2][2] + "\n  - Location: " + liste[2][3] + "\n  - Organiser: " + liste[2][4] + "\n  - Language: " + liste[2][5] + "\n  - Participants: " + liste[2][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[2] + u"\u0022" + " >More Info</a>"
	msgid = (chat_id21, inlinedata.get(chat_id21))
	t_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=' 1 ', callback_data='edit1'),InlineKeyboardButton(text='< 2 >', callback_data='edit2'),InlineKeyboardButton(text=' 3 ', callback_data='edit3'),InlineKeyboardButton(text=' 4 ', callback_data='edit4')]])
	bot.editMessageText(msgid,message,reply_markup=t_keyboard, parse_mode='HTML' )
	bot.answerCallbackQuery(idsa, text='Convoys List Updated')

# Send the third page from convoys list	

def convoylist2(msg):
	chat_id21 = msg['from']['id']
	idsa = msg['id']
	lista = urllib.urlopen("http://ets2c.com/")
	lista1 = lista.read()
	soup = BeautifulSoup(lista1, "lxml" )
	lista2 = soup.find_all("div", class_="row")[7:10]
	liste = []
	link1 = []
	for i in range(0,3):
		testopreso1 = lista2[i].getText()
		testopreso2 = testopreso1.replace("<","")
		testopreso = testopreso2.replace(">","")
		listaelaborata = testopreso.split("\n")
		liste.append(listaelaborata)
		i += 1
	for link in soup.find_all('a')[18:21]:
			link1.append(link.get('href'))
	basta = u"\U0001f537"
	message = u"\u2757\ufe0f" + " Upcoming Events " + u"\u2757\ufe0f" + "\n\n"
	message += basta + " Server: " + liste[0][1] + "\n  - Time: " + liste[0][2] + "\n  - Location: " + liste[0][3] + "\n  - Organiser: " + liste[0][4] + "\n  - Language: " + liste[0][5] + "\n  - Participants: " + liste[0][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[0] + u"\u0022" + " >More Info</a>"  + "\n\n"
	message += basta + " Server: " + liste[1][1] + "\n  - Time: " + liste[1][2] + "\n  - Location: " + liste[1][3] + "\n  - Organiser: " + liste[1][4] + "\n  - Language: " + liste[1][5] + "\n  - Participants: " + liste[1][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[1] + u"\u0022" + " >More Info</a>"  + "\n\n"
	message += basta + " Server: " + liste[2][1] + "\n  - Time: " + liste[2][2] + "\n  - Location: " + liste[2][3] + "\n  - Organiser: " + liste[2][4] + "\n  - Language: " + liste[2][5] + "\n  - Participants: " + liste[2][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[2] + u"\u0022" + " >More Info</a>"
	msgid = (chat_id21, inlinedata.get(chat_id21))
	t_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=' 1 ', callback_data='edit1'),InlineKeyboardButton(text=' 2 ', callback_data='edit2'),InlineKeyboardButton(text='< 3 >', callback_data='edit3'),InlineKeyboardButton(text=' 4 ', callback_data='edit4')]])
	bot.editMessageText(msgid,message,reply_markup=t_keyboard, parse_mode='HTML' )
	bot.answerCallbackQuery(idsa, text='Convoys List Updated')

# Send the fourth page from convoys list

def convoylist3(msg):
	chat_id21 = msg['from']['id']
	idsa = msg['id']
	lista = urllib.urlopen("http://ets2c.com/")
	lista1 = lista.read()
	soup = BeautifulSoup(lista1, "lxml" )
	lista2 = soup.find_all("div", class_="row")[10:13]
	liste = []
	link1 = []
	for i in range(0,3):
		testopreso1 = lista2[i].getText()
		testopreso2 = testopreso1.replace("<","")
		testopreso = testopreso2.replace(">","")
		listaelaborata = testopreso.split("\n")
		liste.append(listaelaborata)
		i += 1
	for link in soup.find_all('a')[21:24]:
			link1.append(link.get('href'))
	basta = u"\U0001f537"
	message = u"\u2757\ufe0f" + " Upcoming Events " + u"\u2757\ufe0f" + "\n\n"
	message += basta + " Server: " + liste[0][1] + "\n  - Time: " + liste[0][2] + "\n  - Location: " + liste[0][3] + "\n  - Organiser: " + liste[0][4] + "\n  - Language: " + liste[0][5] + "\n  - Participants: " + liste[0][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[0] + u"\u0022" + " >More Info</a>"  + "\n\n"
	message += basta + " Server: " + liste[1][1] + "\n  - Time: " + liste[1][2] + "\n  - Location: " + liste[1][3] + "\n  - Organiser: " + liste[1][4] + "\n  - Language: " + liste[1][5] + "\n  - Participants: " + liste[1][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[1] + u"\u0022" + " >More Info</a>" + "\n\n"
	message += basta + " Server: " + liste[2][1] + "\n  - Time: " + liste[2][2] + "\n  - Location: " + liste[2][3] + "\n  - Organiser: " + liste[2][4] + "\n  - Language: " + liste[2][5] + "\n  - Participants: " + liste[2][6] + "\n  - <a href=" + u"\u0022" + "http://ets2c.com/" + link1[2] + u"\u0022" + " >More Info</a>"
	msgid = (chat_id21, inlinedata.get(chat_id21))
	t_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=' 1 ', callback_data='edit1'),InlineKeyboardButton(text=' 2 ', callback_data='edit2'),InlineKeyboardButton(text=' 3 ', callback_data='edit3'),InlineKeyboardButton(text='< 4 >', callback_data='edit4')]])
	bot.editMessageText(msgid,message,reply_markup=t_keyboard, parse_mode='HTML' )
	bot.answerCallbackQuery(idsa, text='Convoys List Updated')

# Bring the message to the right function

def spartirichieste(msg):
	try:
		chat_id = msg['chat']['id']
		if chat_id not in usersblocked or usersblocked[chat_id] == False:
			usersblocked[chat_id] = True
			timer = Timer(3, noblock, args=(chat_id,))
			timer.start()
			if msg['text'] == "/start":
				start(msg)
			elif " Servers Stats" in msg['text']:
				serversstats(msg)
			elif " Game Time" in msg['text']:
				gametime(msg)
			elif " Kat_pw Stream Preview" in msg['text']:
				gettwitch(msg)
			elif " Convoys List" in msg['text']:
				convoylist(msg)
			elif "General Information" in msg['text']:
				geninformation(msg)
			elif msg['text'] == "/restart":
				restart(msg)
			elif serverboolean[chat_id] == True:
				serversstats1(msg)
		else:
			bot.sendMessage(msg['chat']['id'],"Please wait some seconds.")
	except KeyError:
		pass
	try:
		datamess = msg['data']
		if datamess == "edit1":
			convoylist11(msg)
		elif datamess == "edit2":
			convoylist1(msg)
		elif datamess == "edit3":
			convoylist2(msg)
		elif datamess == "edit4":
			convoylist3(msg)
	except KeyError:
		pass

# Infinite loop that check for updates
	
bot.message_loop(callback=spartirichieste, run_forever=True)


