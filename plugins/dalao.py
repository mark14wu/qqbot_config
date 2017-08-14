# -*- coding: utf-8 -*-
dict_dalao = {}
group_list = ["596776383", "513096350", "54840756", "662936261"]
# 596776383 = EFZers_2020!
# 513096350 = 1/2EFZers
# 54840756 = EFZ
# 662936261 = 2020届6班
dalao_keywords = ['膜', '大佬', '巨佬', 'dalao', '%']
def onQQMessage(bot, contact, member, content):

	if not contact.qq in group_list:
		return

	if content[:5] == '大佬值查询':
		query_name = content[6:]
		return dalao_query(bot, contact, member, query_name)
	
	dalao_flag = False

	for keyword in dalao_keywords:
		if keyword in content:
			dalao_flag = True

	if not dalao_flag:
		return

	name = member.name

	if name not in dict_dalao.keys():
		dict_dalao[name] = 0

	dict_dalao[name] += 1

	bot.SendTo(contact, name +' 的大佬值+1！')

def dalao_query(bot, contact, member, name):
	bot.SendTo(contact, name +' 的大佬值是 ' + str(dict_dalao[name]))

