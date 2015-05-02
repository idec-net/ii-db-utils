#!/usr/bin/env python2
#-*- coding: utf8 -*-

from ii_functions import *
import base64, sys

args=sys.argv[1:]
if(len(args)==0):
	print "Usage: ii-bundle.py <bundle file>"
	sys.exit(1)

echo=raw_input("Введите нужную эху(эхи): ").decode("utf8").split(" ")

bundle=""

for echoarea in echo:
	msglist=getMsgList(echoarea)
	for msgid in msglist:
		msg=open(msgdir+msgid).read()
		bundle+=msgid+":"+base64.b64encode(msg)+"\n"

try:
	output=open(args[0], "w")
	output.write(bundle)
	output.close()
except:
	print "Не могу открыть файл для записи!"
	sys.exit(1)
