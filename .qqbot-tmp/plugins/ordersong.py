# -*- coding: utf-8 -*-
import pycurl
from io import BytesIO
from urllib.parse import urlencode
import sys
group_list = ["596776383", "513096350", "54840756"]
order_keywords = ['点歌', '来一首', '来首']
def onQQMessage(bot, contact, member, content):
	if content[:2] in order_keywords and contact.qq in group_list:
		user_input = content[3:]
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
		body = body.decode('iso-8859-1')
		null = 0
		body = eval(body)
		id = body['result']['songs'][0]['id']
		# order_content = "http://music.163.com/#/song?id=" + str(id)
		order_content2 = "http://music.163.com/song/" + str(id) + "?userid=52663812"
		bot.SendTo(contact, order_content2)
		# print('\n')
		# print(order_content)
		# except:
		# 	bot.SendTo(contact, '点歌' + songname + '失败！')
