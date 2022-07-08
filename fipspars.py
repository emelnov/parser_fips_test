import random
import requests
from bs4 import BeautifulSoup, Comment
import time
import urllib
import os
import json
from dicttoxml import dicttoxml
import xml.etree.ElementTree as ET


def FindByNum( mainpage, dict_el, findnum):
	contents = mainpage.find_all('span', {'id':'content_title_num'})
	for content in contents:
		if content.text.strip() == findnum:
			dict_el = content.parent.findChildren()[3].text
	return dict_el		


def LoadUserAgents(uafile=''):
	uas = []
	with open(uafile, 'rb') as uaf:
		for ua in uaf.readlines():
			if ua:
				uas.append(ua.strip()[1:-1-1])
	random.shuffle(uas)
	return uas
	
def create_path(src):
	path = src
	filename = src[src.rfind("/")+1:]
	dir = src.replace("/"+filename, "")
	dir_path  = 'parsed_data'+"/"+dir
	if os.path.exists(dir_path)==False:
		os.makedirs(dir_path)
	return {'filename':filename, 'dir_path':dir_path, 'path':path}
	
	
def download(url, filepath):	

	headers = {
		"User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.4; Nexus 7 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36"
		}	
	
	url = url.replace("https://www1.fips.ru/", "https://fips.ru/")
	try:
		response = requests.get(url, headers=headers)
		filepath = filepath.replace('//', '/')
		file = open(filepath, "wb")
		file.write(response.content)
		file.close()
	except:
		# opener = urllib.request.build_opener()
		# opener.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 7 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36')]
		# urllib.request.install_opener(opener)
		urllib.request.urlretrieve(url, filepath)
	time.sleep(3)	
	return True
	
	
user_agents = LoadUserAgents(uafile="user_agent.txt")
# headers = {
	# "User-Agent" : random.choice(user_agents)
	# }
headers = {
	"User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.4; Nexus 7 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36"
	}	
	



pagenum = 226
i = 2000
while True:
	
	

	url = "https://www.fips.ru/publication-web/publications/UsrTM?pageNumber="+str(pagenum)+"&inputSelectOIS=TM,CKTM,AOG,ERAOG,TMIR&tab=UsrTM&searchSortSelect=dtPublish&searchSortDirection=true"	
	
	
	## В случа если нужно через прокси, понадобится прокси лист	
	# user_agent = random.choice(user_agents)
	# headers = {
		# "User-Agent" : user_agent
		# }
	# try:
		# r = requests.get(url, proxies=proxy, headers=headers)
	# except:
		# print  ( "Ошибка при соединении пропускаем, ждём 40 секунд" )
		# time.sleep(40)
		# continue
		
	r = requests.get(url, headers=headers)	
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text, 'lxml')
	
	table = soup.find('div',{'class':'bgtable'}).find('table',{'class':'table'})

	anonses  = table.findChildren("table")

	record = {}
	if i % 100 == 0 or i == 2000:
		st_n = i
		to_n = i + 100
		step_folder_name = "steps_"+str(st_n)+"-"+str(to_n)
	
	for info in anonses:
		try:
			elements = info.find_all('td')
			####
			## Формируем базововую информацию о публикации на сайте fips.ru
			####
			record['doc_link'] = "https://www.fips.ru/publication-web/publications/"+elements[0].find('a')['href']
			record['doc_num'] = elements[0].text.strip().replace("\n", '').replace("\xa0", '').replace("            ", ' ')
			record['doc_name'] = elements[1].text.strip().replace("\n", ' ')
			
			try:
				path_for_record = create_path(step_folder_name+"/"+record['doc_num'].replace(" ", "_")+"/small_image.jpg")
				record['small_image_link'] = ''
				record['small_image_link'] = elements[2].find('img')['src']
				download(record['small_image_link'],  './'+path_for_record['dir_path']+'/'+path_for_record['filename'])
			except:
				print ("Нет изображения")
				record['small_image_link'] = ''
				sleep(4)
				
			record['doc_desc'] =  ''
			if len(elements[3].text)>0:
				record['doc_desc'] = elements[3].text.strip().replace("\n", '').replace("         ", ' ')    
			dates =  elements[5].find_all('span',{'class':'mobileblock'})
			record['doc_public_date'] =  dates[0].text.replace(dates[0].find("span").text, "")
			record['doc_reg_date'] =  dates[1].text.replace(dates[1].find("span").text, "")
			try:
				record['pdf_link'] = elements[5].find("a")['href']
				path_for_record = create_path(step_folder_name+"/"+record['doc_num'].replace(" ", "_")+"/document.pdf")
				download(record['pdf_link'] ,  './'+path_for_record['dir_path']+'/'+path_for_record['filename'])
			except:
				print ("Нет pdf_link")
				record['pdf_link'] = ''
				sleep(4)
			####
			## Скачиваем более подробную информацию о публикации fips.ru
			####
			docpage = requests.get(record['doc_link'], headers=headers)	
			docpage.encoding = 'utf-8'
			docpage_soup = BeautifulSoup(docpage.text, 'lxml')
			mainpage = docpage_soup.find('div',{'id':'mainpagecontent'})
			
			try:
				record['big_image_link'] = mainpage.find('img')['src']
				path_for_record = create_path(step_folder_name+"/"+record['doc_num'].replace(" ", "_")+"/big_image.jpg")
				download(record['big_image_link'] ,  './'+path_for_record['dir_path']+'/'+path_for_record['filename'])
			except:
				print ("Нет изображения")
				record['big_image_link'] = ''
				sleep(4)
			
			
			
			record['591_colors'] = ''
			record['591_colors'] = FindByNum( mainpage, record['591_colors'], '(591)')
			record['526_noprotected'] = ''
			record['526_noprotected'] = FindByNum( mainpage, record['526_noprotected'], '(526)')
					
			
			find_mktus = mainpage.find_all('div', {'class':'oneblock-number'})
			record['511_MKTU'] = ''
			for elfind  in find_mktus:
				if "(511) МКТУ" in elfind.text.strip():
					record['511_MKTU'] = elfind.find('span').text.strip()
			
			path_for_record = create_path(step_folder_name+"/"+record['doc_num'].replace(" ", "_")+"/data.json")
			record_json_file = open( './'+path_for_record['dir_path']+'/'+path_for_record['filename'], "w", encoding="utf8")
			record_json_file.write(json.dumps(record))
			record_json_file.close()
			
			path_for_record = create_path(step_folder_name+"/"+record['doc_num'].replace(" ", "_")+"/data.xml")
			record_xml_file = open( './'+path_for_record['dir_path']+'/'+path_for_record['filename'], "wb")
			record_xml_file.write( dicttoxml(record, custom_root='info') )
			record_xml_file.close()
			
			print ("pagenum "+str(pagenum))
			print ("i "+str(i))
			print (record)
			print (step_folder_name)
			i = i + 1		
			time.sleep(6)
		except:	
			print ("Ошибка при разборе , подождём / редко возникает, но обрывает работу. / Пауза одна минута")
			time.sleep(60)
	pagenum = pagenum +1
	
	
	
		
		
		