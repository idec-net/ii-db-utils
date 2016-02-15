#!/usr/bin/env python3

import base64, sys
from ii_functions import *

args=sys.argv[1:]
if len(args)<2:
	print("Usage: ii-debundle.py <bundle file> <base directory>")
	sys.exit(1)

basedir=args[1]
indexdir=os.path.join(basedir, indexdir_name)
msgdir=os.path.join(basedir, msgdir_name)

check_dirs()

bundles=read_file(args[0]).splitlines()
if not bundles:
	print("error opening bundle")
	sys.exit(1)

for bundle in bundles:
	arr=bundle.split(":")
	if(arr[0]!="" and arr[1]!=""):
		msgid=arr[0]; message=b64d(arr[1])
		echo=message.splitlines()[1]
		try:
			savemsg(msgid, echo, message)
			print("savemsg "+msgid)
		except Exception as e:
			print("saving error: "+str(e)+" "+msgid)
			raise
