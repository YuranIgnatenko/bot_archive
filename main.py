''' 
Dev : G E O R G 
''' 
import telebot,random
from telebot import types 

import requests, pyshorteners, os, sys
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlopen

from panel import *
from parser import category_db

token = "Your_token"
isrunsender = False

################################
################################
################################

bot = telebot.TeleBot(token)

def run_online(mcid):
	if (True):
		for i in range(2000):
		 	tmp_b = len(category_db[db_visit_name[mcid]])-1      
		 	tmp_a = random.randint(0,tmp_b)
		 	name = db_visit_name[mcid]
		 	url,r_page,r_href = get_r_page_href(name)
		 	out = get_href_content_online(url,r_page,r_href)
		 	try:
		 		bot.send_photo(mcid,urlopen(out))
		 	except Exception as e:
		 		try:
		 			s = f"{e}".split(" ")[-1].replace("sec","")
		 			bot.send_photo(mcid,urlopen(out))
		 		except Exception:         			
		 			bot.send_message(mcid,text="Некоторые файлы устарели.\nЗапустите обновление файлов\nМеню > Настройки бота > Обновление",reply_markup=panel_control_visit_online(db_visit_name[mcid],r_page,r_href))
		 			
		 		return



def run_sender(mcid):
	tmp_b = 0
	tmp_a = random.randint(0,tmp_b)
	tc = 0
	iter_c = 1000
	for i in range(iter_c):
				name = "Люди"
				tc += 1  	
				db_visit_name[mcid] = name
				url,r_page,r_href = get_r_page_href(name)
				out = get_href_content_online(url,r_page,r_href)
				try:
					bot.send_photo(mcid,urlopen(out))
				except Exception:
					bot.send_message(mcid,text="Некоторые файлы устарели.\nЗапустите обновление файлов\nМеню > Настройки бота > Обновление",reply_markup=panel_control_pack_online(db_visit_name[mcid],r_page,r_href,1,2))     
				

### commands /Any*

@bot.message_handler(commands=['start'])
def start(message):
	global category_db
	mcid = message.chat.id
	db_visit_name[mcid] = ""
	category_db[db_visit_name[mcid]]={}    #category_db[db_visit_name[mcid]][db_visit_index[mcid]] = "null category"
	db_visit_index[mcid] =0
	bot.send_message(mcid, text="ok", reply_markup=panel_menu())

@bot.message_handler(commands=["abort"])
def abort(message):
	global isrunsender
	isrunsender = False
	mcid = message.chat.id
	db_visit_name[mcid] = ""
	category_db[db_visit_name[mcid]]={}
	db_visit_index[mcid] = 0
	bot.send_message(mcid, text="ok", reply_markup=panel_menu())
	sys.exit()
	os.abort()


			
@bot.message_handler(content_types=['text'])
def func(message):
	global isrunsender, category_db
	mi = message.message_id
	mt = message.text
	mcid = message.chat.id
	
	if(mt == "Меню"):
		bot.send_message(mcid, text="ok", reply_markup=panel_menu()) 
	 
 ### menu tree     

	elif(mt in category):
		tmp_b = len(category_db[mt])-1
		tmp_a = db_visit_index[mcid]+1
		db_visit_name[mcid]=mt
		out=category_db[mt][db_visit_index[mcid]]   
		bot.send_message(mcid,text="Выполнено",reply_markup=panel_control_visit(tmp_a,tmp_b,"1","1",mt))
			
	elif(mt[1:] in ["30","15","5","1"]):
		sym = mt[0]
		tmp_d = int(mt[1:])
		tmp_b = len(category_db[db_visit_name[mcid]])-1        
		for i in range(tmp_d):
			if sym == "+":
				tmp_a = db_visit_index[mcid]+1
				tmp_c = i+1
				if i >= tmp_b:return
				db_visit_index[mcid] += 1
			elif(sym == "-"):
				tmp_a = db_visit_index[mcid]+1
				tmp_c = i+1
				if 0-i <= 0-len(category_db[db_visit_name[mcid]]):return
				db_visit_index[mcid] -= 1
			else:pass
		try:
			out=category_db[db_visit_name[mcid]][db_visit_index[mcid]]
		
			bot.send_photo(mcid,urlopen(out))
		except Exception as e:
			bot.send_message(mcid,text="Некоторые файлы устарели.\nЗапустите обновление файлов\nМеню > Настройки бота > Обновление\n\n"+str(e),reply_markup=panel_menu())     
			return    
									
		bot.send_message(mcid,text="ok",reply_markup=panel_control_visit(tmp_a,tmp_b,"1","1",db_visit_name[mcid]))     	
			
	elif mt == "Случайная offline":
		tmp_b = len(category_db[db_visit_name[mcid]])-1        
		tmp_a = random.randint(0,tmp_b)
		db_visit_index[mcid] = tmp_a        
		out=category_db[db_visit_name[mcid]][db_visit_index[mcid]]
		try:
			bot.send_photo(mcid,urlopen(out))
		except Exception:
			bot.send_message(mcid,text="Некоторые файлы устарели.\nЗапустите обновление файлов\nМеню > Настройки бота > Обновление",reply_markup=panel_menu())     
			return     	
							
		bot.send_message(mcid,text="ok",reply_markup=panel_control_visit(tmp_a,tmp_b,"1","1",db_visit_name[mcid]))    		

			
			
			
	elif (mt == "Случайная online" or mt == "Следующая"):
		for i in range(2000):
		 	tmp_b = len(category_db[db_visit_name[mcid]])-1      
		 	tmp_a = random.randint(0,tmp_b)
		 	name = db_visit_name[mcid]
		 	url,r_page,r_href = get_r_page_href(name)
		 	out = get_href_content_online(url,r_page,r_href)
		 	try:
		 		bot.send_photo(mcid,urlopen(out))
		 	except Exception as e:
		 		try:
		 			s = f"{e}".split(" ")[-1].replace("sec","")
		 			bot.send_photo(mcid,urlopen(out))
		 		except Exception:         			
		 			bot.send_message(mcid,text="Некоторые файлы устарели.\nЗапустите обновление файлов\nМеню > Настройки бота > Обновление",reply_markup=panel_control_visit_online(db_visit_name[mcid],r_page,r_href))
		 			
		 		return
			
	elif mt == "Запуск сендера":
		isrunsender = True
		while isrunsender:
			run_sender()
	elif mt == "Online подборка":
		tmp_b = 0   
		tmp_a = random.randint(0,tmp_b)
		tc = 0
		for name in category:      
			tc += 1  	
			db_visit_name[mcid] = name
			url,r_page,r_href = get_r_page_href(name)
			out = get_href_content_online(url,r_page,r_href)
			try:
				bot.send_photo(mcid,urlopen(out))
				bot.send_message(mcid,text=f"{db_visit_name[mcid],r_page,r_href}",reply_markup=panel_control_pack_online(db_visit_name[mcid],r_page,r_href,tc,len(category)))     
			except Exception:
				bot.send_message(mcid,text="Некоторые файлы устарели.\nЗапустите обновление файлов\nМеню > Настройки бота > Обновление",reply_markup=panel_control_pack_online(db_visit_name[mcid],r_page,r_href,1,2))     
				return     	    				                	                bot.send_message(mcid,text="Выполнено",reply_markup=panel_menu())
								
			
	elif mt == "Offline подборка":
		tmp_count_from_visit = 1
		tmp_visit_name_list = []
		tmp_out_list = []
		for i in range(tmp_count_from_visit):
			for tmp_name in category:
				tmp_len = len(category_db[tmp_name])-1     
				tmp_index = random.randint(0,tmp_len)
				tmp_out_list.append(category_db[tmp_name][tmp_index])
		try:
			i = 0
			for out in tmp_out_list:
				i+=1
				bot.send_photo(mcid,urlopen(out))
				bot.send_message(mcid,text=f"{i}/{len(tmp_out_list)}",reply_markup=panel_status_short(i,len(tmp_out_list),"Случайная подборка"))    
		except Exception as e:
			bot.send_message(mcid,text="Некоторые файлы устарели.\nЗапустите обновление файлов\nМеню > Настройки бота > Обновление\n\n"+str(e),reply_markup=panel_menu())     
			return     	        	        		
		bot.send_message(mcid,text="ok",reply_markup=panel_menu())    		

			
	  					 											 										
	elif mt == "Папки с файлами":
		bot.send_message(mcid, text="ok", reply_markup=panel_category_list())
 
			
	elif mt == "Настройки бота":
		bot.send_message(mcid, text="ok", reply_markup=panel_settings_bot())
	
	elif mt == "Обновление (последнее)":
		bot.send_message(mcid, text="Обновление запущено", reply_markup=panel_settings_bot())
		tmpc = 0
		for key in category:
			tmpc+=1
			category_db[key] =get_href_content_range(category_links[key],1,1,bot,mcid,tmpc,len(category_db),key)
			
		save_file_href(category_db)
		bot.send_message(mcid, text="Обновление завершено", reply_markup=panel_settings_bot())
		
			
   
	elif mt == "Обновление (случайный день)":
		bot.send_message(mcid, text="Обновление запущено", reply_markup=panel_settings_bot())
		tmpc = 0
		for key in category:
			tmpc+=1
			rand_day = random.randint(3,get_count_pages(category_links[key]))
			category_db[key] =get_href_content_range(category_links[key],1,1,bot,mcid,tmpc,len(category_db),key)
			
		save_file_href(category_db)
		bot.send_message(mcid, text="Обновление завершено", reply_markup=panel_settings_bot())
		
			
	  
	elif mt == "Обновление (случайная неделя)":
		bot.send_message(mcid, text="Обновление запущено", reply_markup=panel_settings_bot())
		tmpc = 0
		for key in category:
			tmpc+=1
			rand_day = random.randint(3,get_count_pages(category_links[key]))
			category_db[key] =get_href_content_range(category_links[key], rand_day,rand_day+7,bot,mcid,tmpc,len(category_db),key)
			
		save_file_href(category_db)
		bot.send_message(mcid, text="Обновление завершено", reply_markup=panel_settings_bot())
		
			
						
												
	elif mt == "Отчет по хранилищу":
		sum_u = 637282
		sum_f = 0
		for k in category_db:sum_f+=len(category_db[k])
		sum_c = len(category)
		datefile = datetime.fromtimestamp(os.path.getmtime('category_db.txt'))
		sizifile = round(os.path.getsize('category_db.txt')/1024,2)
		updateflag = True #tested
		bot.send_message(mcid, text="Отчет", reply_markup=panel_status_storage(sum_u,sum_f,sum_c,datefile,sizifile,updateflag))

												
	elif mt == "Форматировать хранилище":
		bot.send_message(mcid, text="Удалено 8228 файлов успешно", reply_markup=panel_category_list())
 
					  
					 
print('launch server')
print("bot listen")
							
bot.polling(none_stop=True)