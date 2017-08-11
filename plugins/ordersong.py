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
order_keywords = ['点歌', '来一首', '来首']
rank_keywords = ['点歌', '排行']

def onQQMessage(bot, contact, member, content):
	order_flag = False
	if not contact.qq in group_list:
		return

	if content[:2] in order_keywords:
		user_input = content[3:]
		order_flag = True
	elif content[:3] in order_keywords:
		user_input = content[4:]
		order_flag = True

	if order_flag:
		return search_song(bot, user_input, contact, member, content)

def search_song(bot, user_input, contact, member, content):
	songname = user_input.split('，')[0]
	artist = None
	try:
		artist = user_input.split('，')[1]
	except:
		pass
	sys.stdout.buffer.write(songname.encode('utf8'))
	# try:
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
	# print('\n')
	# print(order_content)
	# except:
	# 	bot.SendTo(contact, '点歌' + songname + '失败！')
	rank_flag = True
