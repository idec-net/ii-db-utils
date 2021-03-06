#!/usr/bin/env python3

import os, sys, shutil, base64
from ii_functions import *

args=sys.argv[1:]
if len(args)==2:
	tobundle=False
elif len(args)==3:
	tobundle=args[2]
else:
	print("Usage: offline-fetch.py <source> <destination> [bundle output file]")
	sys.exit(1)

source=args[0]
dest=args[1]

def echoFromFile(filename):
	if os.path.exists(filename):
		try:
			f=read_file(filename).splitlines()
			return f
		except:
			print("opening error")
			return []
	else:
		return []

def fetch_messages(source, dest, echoesToFetch, tobundle):
	if len(echoesToFetch)==0:
		return []

	if tobundle:
		bundle=""

	for echoarea in echoesToFetch:
		print("fetch "+echoarea)
		sourcepath=os.path.join(source, indexdir_name, echoarea)
		sourceEcho=echoFromFile(sourcepath)

		destpath=os.path.join(dest, indexdir_name, echoarea)
		destEcho=echoFromFile(destpath)

		difference=[msg for msg in sourceEcho if msg not in destEcho]

		for msgid in difference:
			if tobundle:
				msgpath=os.path.join(source, msgdir_name, msgid)
				try:
					bundle+=msgid+":"+base64.b64encode(read_file(msgpath))+"\n"
				except:
					print("Невозможно открыть файл: "+msgpath)
			else:
				try:
					shutil.copyfile(os.path.join(source, msgdir_name, msgid),  os.path.join(dest, msgdir_name, msgid))
					print("savemsg "+msgid)
				except:
					print("Ошибка копирования: "+msgid)

		if len(difference)!=0 and not tobundle:
			print("append message index")
			try:
				f=open(destpath, "a")
				f.write("\n".join(difference)+"\n")
				f.close()
			except:
				print("Ошибка сохранения индекса")

	if tobundle and bundle:
		try:
			f=open(tobundle, "w")
			f.write(bundle)
			f.close()
		except:
			print("Невозможно сохранить бандл!")

echo=input("Введите нужные эхи через пробел (или '*' для всех): ")
if echo=="*":
	echo=os.listdir(os.path.join(source, "echo"))
else:
	echo=echo.split(" ")

if not os.path.exists(os.path.join(dest, indexdir_name)):
	print("Каталог индекса не существует; создаём...")
	os.makedirs(os.path.join(dest, indexdir_name))

if not os.path.exists(os.path.join(dest, msgdir_name)):
	print("Каталог сообщений не существует; создаём...")
	os.makedirs(os.path.join(dest, msgdir_name))

fetch_messages(source, dest, echo, tobundle)
