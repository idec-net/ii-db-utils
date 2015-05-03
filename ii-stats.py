#!/usr/bin/env python2
# -*- coding: utf8 -*-

indexdir="echo/"
msgdir="msg/"

import os
from ii_functions import *

def dirsize(path):
	size=os.path.getsize(path)
	for f in os.listdir(path):
		size+=os.path.getsize(os.path.join(path, f))
	return size

def humansize(size):
	size=float(size)
	b="Б"
	kb="Кб"
	mb="Мб"
	gb="Гб"
	strings=[b, kb, mb, gb]
	_format="%.1f%s"
	for u in strings:
		if size<1024 : return _format % (size, u)
		size/=1024
	return _format % (size, strings)

index=[]
countindex={}
echolist=os.listdir(indexdir)
for echoarea in echolist:
	echo=getMsgList(echoarea)
	countindex[echoarea]=len(echo)
	index+=echo

echoesOrder=sorted(countindex, key=countindex.get, reverse=True)

print "Статистика по эхоконференциям\n===="
for echo in echoesOrder:
	print echo+": "+str(countindex[echo])

print "\nЭхоконференций: "+str(len(echolist))
print "Всего сообщений: "+str(len(index))

if(len(index)<=0):
	print "База пуста (проверьте права доступа)."
	exit()

print "\nЗагрузка базы..."
msglist={}
for x in index:
	msglist[x]=getMsg(x)

print "Размер базы данных:"
indexsize=dirsize(indexdir)
msgs_size=dirsize(msgdir)
print "Индекс: "+humansize(indexsize)+"; Сообщения: "+humansize(msgs_size)+"; Всего: "+humansize(indexsize+msgs_size)+";"

print "\nПо поинтам:\n===="
userlist={}
for msg in msglist.itervalues():
	point=msg.get("sender").encode("utf-8")
	if(not userlist.__contains__(point)):
		userlist[point]=1
	else:
		userlist[point]+=1

usersOrder=sorted(userlist, key=userlist.get, reverse=True)
for point in usersOrder:
	print point+": "+str(userlist[point])

print "\nВсего поинтов: "+str(len(userlist.keys()))
