#pylint:disable=E0602
''' 
Dev : G E O R G 

''' 

import telebot,random,time
from telebot import types 

from bs4 import BeautifulSoup

import os,sys,pyshorteners,requests
from datetime import datetime
from parser import *
from urllib.request import urlopen

token='8165343589:AAE_GUvzzXA1u-JOV4WK0SUanzryndnbVnc'

flagSelectedID = 0
flagSelectedValue = ""
flagDB = {}
flagStarted = {}
flagFileUsers = "users.txt"
flagFileHistoryLogs = "historylogs.txt"
flagPswdAdmin = "1234@"
flagAdminID = 0

################################

msgcode1 = "вход как админ"
msgcode2 = "запуск сендера"
msgcode3 = "запуск бота"
msgcode4 = "не найден в базе"
msgcode5 = "остановка бота"

################################
################################


bot = telebot.TeleBot(token)


def about_links():
	s = ""
	for c in category_links:
		s += f"{c} {get_count_pages(category_links[c])} x 10\n\n"		
	return s


def rec_event(mcid,log):
	return f"[{datetime.now()}] [{mcid}] [{log}]" 

def add_log(record):
	global flagFileHistoryLogs
	with open(flagFileHistoryLogs, 'a')as file:
		file.write(f"{record}\n")

def read_logs():
	global flagFileHistoryLogs
	try:
		with open(flagFileHistoryLogs, 'r')as file:
			data = file.read().split("\n")
			return data
	except FileNotFoundError:
		open(flagFileHistoryLogs, 'w')
		return



def save_userdb(dt):
	global flagFileUsers
	with open(flagFileUsers, 'w')as file:
		for k in dt:
			file.write(f"{k}={dt[k]}\n")

def upload_userdb():
	global flagFileUsers
	global flagDB
	try:
		with open(flagFileUsers, 'r')as file:
			data = file.read().split("\n")
	except FileNotFoundError:
		open(flagFileUsers, 'w')
		return
	for line in data:
		if len(line) < 3:continue
		line = line.split("=")
		k,v = int(line[0]),line[1]
		flagDB[k] = v

def read_userdb():
	global flagDB,flagFileUsers
	try:
		with open(flagFileUsers, 'r')as file:
			data = file.read().split("\n")
			return data
	except FileNotFoundError:
		open(flagFileUsers, 'w')
		return

def run_sender(mcid):
	global flagStart,flagDB
	add_log(rec_event(mcid,msgcode2))
	tmp_b = 0
	tmp_a = random.randint(0,tmp_b)
	tc = 0
	iter_c = 10000
	name = flagDB[mcid]
	for i in range(iter_c):
				if flagStarted[mcid] == False:
					return 1
				tc += 1  	
				db_visit_name[mcid] = name
				url,r_page,r_href = get_r_page_href(name)
				out = get_href_content_online(url,r_page,r_href)
				try:		        	
					bot.send_photo(mcid,urlopen(out))	 
				except Exception as e:
					pass
### commands /Any*


@bot.message_handler(commands=['start'])
def start(message):
	global flagDB
	mcid = message.chat.id
	add_log(rec_event(mcid,msgcode3))
	mcid = int(mcid) 
	upload_userdb()
	if mcid not in flagDB:
		add_log(rec_event(mcid,msgcode4))
		flagDB[mcid] = str(datetime.now())
		save_userdb(flagDB)
	bot.send_message(mcid,text="Управление",reply_markup=panel_user_menu())

			
@bot.message_handler(content_types=['text'])
def func(message):
	global flagStart,flagSelectedID,flagSelectedValue, flagDB,flagAdminID,flagPswdAdmin
	
	mcid = message.chat.id
	mt = message.text
	mn = message.from_user.first_name
		
	if mt == "Запустить":
		flagStarted[mcid] = True	 
		#try:
		run_sender(mcid)
		#iexcept KeyError:
	   #) bot.send_message(mcid,text="Доступ ограничен",reply_markup=panel_no_access_menu())    
			
	if mt == "Остановить":
		 flagStarted[mcid] = False
		 add_log(rec_event(mcid,msgcode5))
				
	if mt == flagPswdAdmin:
		flagAdminID = mcid  
		add_log(rec_event(mcid,msgcode1))
		bot.send_message(mcid,text="Режим Администратора",reply_markup=panel_admin_menu())    	
	
	if flagAdminID != mcid: return
	
	if str(mt).startswith("ID:"):
		val_id = int(mt.split("ID:")[1].split(':')[0])
		flagSelectedID = val_id
		bot.send_message(mcid,text=val_id,reply_markup=panel_admin_set_value())
		
	elif str(mt).startswith("+"):
		val_set = mt
		flagSelectedValue = val_set
		t = f"Применить ?\n\nID:{flagSelectedID}\n{flagSelectedValue}"
		add_log(rec_event(mcid,"изменил доступ на:"+flagSelectedValue))
		bot.send_message(mcid,text=t,reply_markup=panel_admin_set_value())
 
		
	elif mt == "Меню":
		bot.send_message(mcid,text="ок",reply_markup=panel_admin_menu())    	
	elif mt == "Управление доступом":
		bot.send_message(mcid,text="Список Users ID",reply_markup=panel_admin_users(flagDB))      	
	elif mt == "Сохранить":
		flagDB[flagSelectedID] = flagSelectedValue
		save_userdb(flagDB)
		add_log(rec_event(mcid,"сохранен с задачей"+flagSelectedValue))
		bot.send_message(mcid,text="Выполнено !",reply_markup=panel_admin_users(flagDB))  
		 
	elif mt == "Отчет логи":
		data = read_logs() 
		s = ""
		for line in data:
			s += line+"\n\n"  	
		bot.send_message(mcid,text=f"{s}",reply_markup=panel_admin_menu())
	elif mt == "Отчет пользователи":
		data = read_userdb() 
		s = ""
		for line in data:
			s += line+"\n\n"  	
		bot.send_message(mcid,text=f"{s}",reply_markup=panel_admin_menu())
	elif mt == "Отчет по ссылкам":
		bot.send_message(mcid,text=f"{about_links()}",reply_markup=panel_admin_menu())    	


print('launch server')
print("bot listen")
							
bot.polling(none_stop=True)