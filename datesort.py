#!/usr/bin/python2
# -*- coding:utf8 -*-
from ii_functions import *
import os

echolist=os.listdir(indexdir)

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
	
	open("echo_new/"+echo, "w").write("\n".join(msgids)+"\n")
