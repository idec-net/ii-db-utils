#!/usr/bin/python2
# -*- coding:utf8 -*-
from ii_functions import *
import os

echolist=os.listdir(indexdir)

for echo in echolist:
	print("doing "+echo)
	msgids=getMsgList(echo)
	msgs={}
	arr=[]
	doubles=0

	for msgid in msgids:
		msg=getMsg(msgid)
		msgs[msgid]=msg

		if [msg["msg"], msg["subj"]] in arr:
			doubles+=1
			msgids.remove(msgid)
			print msgid
		else:
			arr.append([msg["msg"], msg["subj"]])
	
	if doubles>0:
		print("doubles: "+str(doubles))
		open("echo_new/"+echo, "w").write("\n".join(msgids)+"\n")
