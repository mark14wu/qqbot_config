# -*- coding: utf-8 -*-
import pycurl
from io import BytesIO
from urllib.parse import urlencode
import sys
group_list = ["596776383", "513096350", "54840756", "662936261"]
# 596776383 = EFZers_2020!
# 513096350 = 1/2EFZers
# 54840756 = EFZ
# 662936261 = 2020届6班
order_keywords = ['点歌', '来一首', '来首', '点首']
# rank_keywords = ['点歌', '排行']
rank_keywords = ['rank']
orders = {}

class Order(object):
	def __init__(self, membername):
		self.membername = membername
		self.dict_songs = {}
		self.dict_keys = {}
		self.songnumber = 0

	def add(self, keyword, songname):
		self.songnumber += 1
		if keyword not in self.dict_keys:
			self.dict_keys[keyword] = 0
		self.dict_songs[keyword] = songname
		self.dict_keys[keyword] += 1

	def getname(self):
		return self.membername

	def getnum(self):
		return self.songnumber

def rank_query_mostorder(bot, contact, member, content):
	rank_list = sorted(orders.values(), key=lambda item: item.songnumber, reverse=True)
	no1_guy = rank_list[0]
	rank_content = '今日点歌王是：' + no1_guy.getname() + '，ta点了 ' + str(no1_guy.getnum()) + ' 首歌！真厉害！'
	bot.SendTo(contact, rank_content)
	# key_list = sorted(no1_guy.dict_keys.items(), key=lambda key, item: item, reverse=True)
	# if key_list[0]
	# rank_content2 = '其中，他点的最多的'

def onQQMessage(bot, contact, member, content):
	order_flag = False
	rank_flag = True
	if not contact.qq in group_list:
		return

	if content[:2] in order_keywords:
		user_input = content[3:]
		order_flag = True
	elif content[:3] in order_keywords:
		user_input = content[4:]
		order_flag = True

	for rank_keyword in rank_keywords:
		if rank_keyword not in content:
			rank_flag = False

	if order_flag:
		return search_song(bot, user_input, contact, member, content)

	if rank_flag:
		return rank_query_mostorder(bot, contact, member, content)

def search_song(bot, user_input, contact, member, content):
	songname = user_input.split('，')[0]
	artist = None
	try:
		artist = user_input.split('，')[1]
	except:
		pass
	post_data = {'s': songname, 'limit': 10, 'type': 1, 'offset': 0}
	postfields = urlencode(post_data)
	buffer = BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, 'http://music.163.com/api/search/get/')
	c.setopt(c.WRITEDATA, buffer)
	c.setopt(pycurl.COOKIEFILE, "appver=1.5.2;")
	c.setopt(c.POSTFIELDS, postfields)
	c.perform()
	c.close()
	body = buffer.getvalue()
	body = body.decode('utf-8')
	null = 0
	body = eval(body)
	id = body['result']['songs'][0]['id']
	name = body['result']['songs'][0]['name']
	artists = body['result']['songs'][0]['artists']
	artists_list_string = ""
	for artist in artists:
		artists_list_string += artist['name'] + ', '
	artists_list_string = artists_list_string[:-2]
	# order_content = "http://music.163.com/#/song?id=" + str(id)
	order_content1 = member.name +' 点了一首 ' + artists_list_string + ' 的 ' + name +' 送给大家！'
	order_content2 = "http://music.163.com/song/" + str(id) + "?userid=52663812"
	bot.SendTo(contact, order_content1)
	bot.SendTo(contact, order_content2)
	if not member.name in orders:
		orders[member.name] = Order(member.name)
	orders[member.name].add(songname, name)
