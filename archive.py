#!/usr/bin/env python3

import sys, calendar, datetime, time
from ii_functions import *

args=sys.argv[1:]

if len(args) < 2:
	print("Usage: archive.py echoarea YYYY.MM.DD")
	quit()

date = args[1].split(".")
date = calendar.timegm(datetime.date(int(date[0]), int(date[1]), int(date[2])).timetuple())

echoarea = getMsgList(args[0])

if len(echoarea) == 0:
	print("Echoarea is empty or it does not exist.")
	sys.exit(1)

bundle = ""

for msgid in echoarea:
	if len(msgid) == 20:
		msg=read_file(msgdir+msgid)

	if msg == "":
		print("msgid " + msgid + " is empty, continue")
		continue

	msgdate = int(getMsg(None, from_string=msg)["time"])

	if msgdate < date:
		print("saving " + msgid)
		bundle += msgid+":"+b64c(msg)+"\n"

filename=args[0] + "_" + args[1] + "_" + str(int(time.time())) + ".bundle"

try:
	output=open(filename, "w")
	output.write(bundle)
	output.close()
	print("Бандл сохранён под именем "+ filename)
except:
	print("Не могу открыть файл "+ filename +" для записи!")
	sys.exit(1)