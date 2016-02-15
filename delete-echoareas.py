#!/usr/bin/env python3

import os,sys
from ii_functions import *

args=sys.argv[1:]
verbose=True
promt=False

if "-q" in args:
	verbose=False

if "-i" in args:
	promt=True

echo=input("Введите нужную эху(эхи): ").split(" ")
if promt:
	reply=input("Введите yes, если хотите удалить все эти эхи вместе с сообщениями: ")
	if reply!="yes":
		print("Выходим")
		sys.exit(1)

for echoarea in echo:
	if verbose:
		print("Удаляем "+echoarea)
	msglist=getMsgList(echoarea)
	for msgid in msglist:
		delete(os.path.join(msgdir, msgid), verbose)
	delete(os.path.join(indexdir, echoarea), verbose)
