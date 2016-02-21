#!/usr/bin/env python3

import os
from ii_functions import *

check_dirs()

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
	_format="%.1f %s"
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

print("Статистика сообщений по эхам\n====")
lens=[len(s) for s in echoesOrder]
width=max(lens)+2

for echo in echoesOrder:
	print(echo.ljust(width)+str(countindex[echo]))

if(len(index)<=0):
	print("База пуста (проверьте права доступа).")
	exit()

print("\nЗагрузка базы...")
msglist={}
for x in index:
	msglist[x]=getMsg(x)

indexsize=dirsize(indexdir)
msgs_size=dirsize(msgdir)

print("\nПо поинтам\n====")
userlist={}
for msg in msglist.values():
	point=msg.get("sender")
	if(not userlist.__contains__(point)):
		userlist[point]=1
	else:
		userlist[point]+=1

usersOrder=sorted(userlist, key=userlist.get, reverse=True)

lens=[len(s) for s in usersOrder]
width=max(lens)+2

for point in usersOrder:
	print(point.ljust(width)+str(userlist[point]))

strl=18 # на сколько символов рассчитываем

print("\n"+"Эхоконференций".ljust(strl)+": "+str(len(echolist)))
print("Всего сообщений".ljust(strl)+": "+str(len(index)))
print("Всего поинтов".ljust(strl)+": "+str(len(userlist.keys())))
print("Индекс".ljust(strl)+": "+humansize(indexsize))
print("Сообщения".ljust(strl)+": "+humansize(msgs_size))
print("Всего".ljust(strl)+": "+humansize(indexsize+msgs_size))
