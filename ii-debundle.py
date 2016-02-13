#!/usr/bin/env python2
#-*- coding: utf8 -*-

from ii_functions import *
import base64, sys

def target_savemsg(basedir, hash, echo, message):
	echopath=os.path.join(basedir, indexdir_name, echo)
	msgidpath=os.path.join(basedir, msgdir_name, hash)
	
	touch(echopath)
	touch(msgidpath)
	
	open(msgidpath, "w").write(message)
	open(echopath, "a").write(hash+"\n")

args=sys.argv[1:]
if(len(args)<2):
	print "Usage: ii-bundle.py <bundle file> <base directory>"
	sys.exit(1)

bundles=open(args[0]).read().splitlines()
if not bundles:
	print "error opening bundle"
	sys.exit(1)

for bundle in bundles:
	arr=bundle.split(":")
	if(arr[0]!="" and arr[1]!=""):
		msgid=arr[0]; message=b64d(arr[1])
		echo=message.splitlines()[1]
		try:
			target_savemsg(args[1], msgid, echo, message)
			print "savemsg "+msgid
		except:
			print "saving error: "+msgid
