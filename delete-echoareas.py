#!/usr/bin/env python2
#-*- coding: utf8 -*-

import os,sys
from ii_functions import *

def delete(filename, verbose):
	if(not os.path.exists(filename)):
		if (verbose):
			print u"Файл "+filename+u" не существует!"
		return
	try:
		os.remove(filename)
	except:
		if(verbose):
			print u"Ошибка удаления, проверьте права"

args=sys.argv[1:]
verbose=True
promt=False

if ("-q" in args):
	verbose=False

if ("-i" in args):
	promt=True

echo=raw_input("Введите нужную эху(эхи): ").decode("utf8").split(" ")
if(promt):
	reply=raw_input("Введите yes, если хотите удалить все эти эхи вместе с сообщениями: ").decode("utf8")
	if(reply!="yes"):
		print "Выходим"
		sys.exit(1)

for echoarea in echo:
	if (verbose):
		print u"Удаляем "+echoarea
	msglist=getMsgList(echoarea)
	for msgid in msglist:
		if(verbose):
			print "trying "+msgid
		delete(os.path.join(msgdir, msgid), verbose)
	delete(os.path.join(indexdir, echoarea), verbose)
