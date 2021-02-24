#this is for python3.5.2 경로표현에서 차이있음.
import sys
import os
import json
import requests
import telegram
from bs4 import BeautifulSoup


def get_json():
	json_name = sys.argv[0][:-2] + "json"
	if not os.path.exists(json_name):
		print(json_name, " isn't exist\n")
		exit()
	with open(json_name, 'r', encoding='utf-8') as json_file:
		js_string = json_file.read()
		js_dic = json.loads(js_string)
		return js_dic


def set_json(json_data):
	json_name = sys.argv[0][:-2] + "json"
	with open(json_name, 'w', encoding='utf-8') as make_file:
		json.dump(json_data, make_file, ensure_ascii=False, indent="\t")


def telegram_send(json_data, message):
	my_token = json_data["telegram"]["bot_token"]
	bot = telegram.Bot(token=my_token)
	bot.sendMessage(chat_id=json_data["telegram"]["dst_id"], text=message)


def get_title(json_data, soup):
	return soup.select(json_data["board_select"])


def get_id_num(json_data, soup):
	return soup.select(json_data["id_num_select"])


def get_soup(json_data, page_num):
	s = requests.Session()
	json_data["obj_to_send"]['go_page']["paginationInfo.currentPageNo"] = page_num
	s.post(json_data["login_url"], data = json_data['obj_to_send']['login'])
	s.post(json_data["go_url"], data=json_data['obj_to_send']['go_page'])
	res = s.get(json_data["go_url"])
	soup = BeautifulSoup(res.text, "html.parser")
	return soup


def first_run_init(json_data):
	if json_data["last_id_num"] == 0:
		soup = get_soup(json_data, 1)
		newest_id_num = int(get_id_num(json_data, soup)[0].get("value"))
		json_data = get_json()
		json_data["last_id_num"] = newest_id_num
		set_json(json_data)
		print("최초시행 끝")
		exit()


def make_new_board(json_data):
	last_id = json_data["last_id_num"]
	new_board = {}
	page = 0
	newest_id = 0
	running = True
	#아래 한줄은 디버깅을 위해 추가한 구문임.
	new_board["last_id"] = last_id
	while running:
		page += 1
		soup = get_soup(json_data, page)
		id_num_table = get_id_num(json_data, soup)
		title_table = get_title(json_data, soup)
		for r in range(len(id_num_table)):
			now_id = int(id_num_table[r].get("value"))
			if newest_id == 0:
				newest_id = now_id
			if last_id >= now_id:
				running = False
				break
			now_title = title_table[r].select('td')[1].select("a > span")[0].text
			new_board[now_id] = now_title
	json_data["last_id_num"] = newest_id
	set_json(json_data)
	return new_board
