#!/usr/bin/env python3

from ii_functions import *
import sys, calendar, datetime, os

args=sys.argv[1:]

if len(args) < 2:
	print("Usage: clean.py echoarea YYYY.MM.DD")
	quit()

date = args[1].split(".")
date = calendar.timegm(datetime.date(int(date[0]), int(date[1]), int(date[2])).timetuple())

echoarea = getMsgList(args[0])

if len(echoarea) == 0:
	print("Echoarea is empty or it does not exist.")
	sys.exit(1)

clean_echoarea = []

for msgid in echoarea:
	if len(msgid) == 20:
		msg=read_file(msgdir+msgid)

	if msg == "":
		print("msgid " + msgid + " is empty, continue")
		continue

	msgdate = int(getMsg(None, from_string=msg)["time"])

	if msgdate >= date:
		print("append "+ msgid)
		clean_echoarea.append(msgid)
	else:
		delete(os.path.join(msgdir, msgid), verbose=True)

clean_echoarea.append("")
open(indexdir + args[0], "w").write("\n".join(clean_echoarea))