#!/usr/bin/env python3

import base64, sys
from ii_functions import *

args=sys.argv[1:]
if len(args)==0:
	print("Usage: ii-bundle.py <bundle file>")
	sys.exit(1)

check_dirs()

echo=input("Введите нужные эхи через пробел: ").split(" ")

bundle=""

for echoarea in echo:
	msglist=getMsgList(echoarea)
	for msgid in msglist:
		msg=read_file(msgdir+msgid)
		bundle+=msgid+":"+b64c(msg)+"\n"

try:
	output=open(args[0], "w")
	output.write(bundle)
	output.close()
except:
	print("Не могу открыть файл для записи!")
	sys.exit(1)
