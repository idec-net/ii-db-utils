#!/usr/bin/env python2
# -*- coding:utf8 -*-
from ii_functions import *
import os,sys,shutil,base64

args=sys.argv[1:]
if (len(args)==2):
	tobundle=False
elif (len(args)==3):
	tobundle=args[2]
else:
	print "Usage: offline-fetch.py <source> <destination> [bundle output file]"
	sys.exit(1)

source=args[0]
dest=args[1]

def echoFromFile(filename):
	if(os.path.exists(filename)):
		try:
			f=open(filename).read().decode('utf-8').splitlines()
			return f
		except:
			print "opening error"
			return []
	else:
		return []

def fetch_messages(source, dest, echoesToFetch, tobundle):
	if(len(echoesToFetch)==0):
		return []
	
	if(tobundle):
		bundle=""
	
	for echoarea in echoesToFetch:
		print "fetch "+echoarea
		sourcepath=os.path.join(source, indexdir, echoarea)
		sourceEcho=echoFromFile(sourcepath)

		destpath=os.path.join(dest, indexdir, echoarea)
		destEcho=echoFromFile(destpath)

		difference=[msg for msg in sourceEcho if msg not in destEcho]

		for msgid in difference:
			if (tobundle):
				msgpath=os.path.join(source, msgdir, msgid)
				try:
					bundle+=msgid+":"+base64.b64encode(open(msgpath).read())+"\n"
				except:
					print u"Невозможно открыть файл: "+msgpath
			else:
				try:
					shutil.copyfile(os.path.join(source, msgdir, msgid),  os.path.join(dest, msgdir, msgid))
					print "savemsg "+msgid
				except:
					print u"Ошибка копирования: "+msgid
	
		if (len(difference)!=0 and not tobundle):
			print "append message index"
			try:
				f=open(destpath, "a")
				f.write("\n".join(difference)+"\n")
				f.close()
			except:
				print u"Ошибка сохранения индекса"
	
	if (tobundle and bundle):
		try:
			f=open(tobundle, "w")
			f.write(bundle)
			f.close()
		except:
			print u"Невозможно сохранить бандл!"

echo=raw_input("Введите нужную эху(эхи): ").decode("utf8").split(" ")

if not os.path.exists(os.path.join(dest, "echo")):
	print "Каталог индекса не существует; создаём..."
	os.makedirs(os.path.join(dest, "echo"))

if not os.path.exists(os.path.join(dest, "msg")):
	print "Каталог сообщений не существует; создаём..."
	os.makedirs(os.path.join(dest, "msg"))

fetch_messages(source, dest, echo, tobundle)
