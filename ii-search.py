#!/usr/bin/env python3

import os, sys, datetime
from ii_functions import *

dformat="%Y%m%d" # format for date input

def getReadableMsg(msg):
	msgid=msg.get('id')
	subj=msg.get('subj')
	sender=msg.get('sender')
	addr=msg.get('addr')
	to=msg.get('to')

	if msg['repto']:
		repto=msg.get("repto")
	else:
		repto="-"

	msgtext="msgid: "+msgid+"\n"+u"Ответ на: "+repto+"\n"+formatDate(msg.get('time'))+"\n"+subj+"\n"+sender+" ("+addr+")  ->  "+to+"\n\n"+msg.get("msg")
	return msgtext
def sortByTime(msg):
	return float(msg.get("time"))

check_dirs()

echo=input("Введите нужную эху(эхи): ").split(" ")
senders=input("Введите поинтов-отправителей (разделитель ||): ").split("||")
receivers=input("Введите поинтов-получателей (разделитель ||): ").split("||")
address=input("Адрес станции поинта (разделитель ||): ").split("||")
timeprom=input("Введите промежуток времени в формате '20140805 20140920': ").split(" ")
subj=input("Введите тему сообщения: ")
text=input("Введите строку для поиска: ")

dateone=datetime.datetime(1970,1,1)
datetwo=datetime.datetime.today()
if len(timeprom)==2:
	dateone=datetime.datetime.strptime(timeprom[0], dformat)
	datetwo=datetime.datetime.strptime(timeprom[1], dformat)

index=[]
if not echo[0]:
	for echoarea in os.listdir(indexdir):
		index+=getMsgList(echoarea)
else:
	for x in echo:
		index+=getMsgList(x)

if len(index)<=0:
	print("База пуста (проверьте права доступа).")
	exit()

print("Загрузка базы...")
msglist={}
removelist=[]
for x in index:
	msglist[x]=getMsg(x)

print("Фильтрация сообщений...\n")
for msg in msglist.values():
	c=False
	for point in senders:
		if str(point) in msg["sender"]:
			c=True
			break
	d=False
	for addr in address:
		if str(addr) in msg["addr"]:
			d=True
			break
	e=False
	for point in receivers:
		if str(point) in msg["to"]:
			e=True
			break

	msgdate=datetime.datetime.fromtimestamp(float(msg.get("time")))

	if (
		(c and d and e) is False or
		(subj not in msg["subj"]) or
		(text not in msg["msg"]) or
		(msgdate<dateone) or
		(msgdate>datetwo)
	):
		if msg.get("id"):
			removelist.append(msg["id"])

for i in removelist:
	msglist.__delitem__(i)

if len(msglist)==0:
	print("Сообщения не найдены.")
else:
	print("Найдено сообщений: "+str(len(msglist)))
	for msg in sorted(msglist.values(), key=sortByTime):
		print("====----====")
		print(getReadableMsg(msg))

	args=sys.argv[1:]
	if len(args)==1:
		try:
			f=open(args[0], "w")
			f.write("\n".join(msglist)+"\n")
			f.close()
		except Exception as e:
			print("Ошибка записи в файл: "+str(e))
