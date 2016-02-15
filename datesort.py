#!/usr/bin/python3

import os
from ii_functions import *

check_dirs()
echolist=os.listdir(indexdir)

newdir=os.path.join(cwd, "echo_new/")

if not os.path.exists(newdir):
	os.makedirs(newdir)

for echo in echolist:
	print("doing "+echo)
	msgids=getMsgList(echo)
	msgs={}

	for msgid in msgids:
		msg=getMsg(msgid)
		msg["time"]=int(msg["time"])
		msgs[msgid]=msg

	def sortTime(msgid):
		return msgs[msgid].get("time")

	msgids.sort(key=sortTime)

	open(newdir+echo, "w").write("\n".join(msgids)+"\n")
