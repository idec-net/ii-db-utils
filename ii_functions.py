#!/usr/bin/env python3

import os, base64, datetime, hashlib

cwd = os.getcwd()

indexdir_name="echo/"
msgdir_name="msg/"

indexdir=os.path.join(cwd, indexdir_name)
msgdir=os.path.join(cwd, msgdir_name)

def read_file(filename):
	with open(filename, "rb") as p:
		return p.read().decode("utf8")

def getMsg(msgid):
	global msgdir
	try:
		msg=read_file(msgdir+msgid).splitlines()
		tags=parseTags(msg[0])
		if 'repto' in tags:
			rpt=tags['repto']
		else:
			rpt=False

		message="\n".join(msg[8:])

		meta=dict(repto=rpt,tags=tags,echo=msg[1],time=msg[2],sender=msg[3],addr=msg[4],to=msg[5],subj=msg[6],msg=message,id=msgid)
	except:
		meta=dict(repto=False,tags="",echo="",time=0,sender="",addr="",to="",subj="",msg="no message",id=msgid)
	return meta

def b64c(string):
	return base64.b64encode(string.encode("utf8")).decode("utf8")

def b64d(str):
	return base64.b64decode(str).decode("utf8")

def hsh(str):
	return base64.urlsafe_b64encode( hashlib.sha256(bytes(str, "utf8")).digest() ).decode("utf8").replace('-','A').replace('_','z')[:20]

def touch(fname):
	if os.path.exists(fname):
		os.utime(fname, None)
	else:
		open(fname, 'a').close()

def savemsg(hash, echo, message):
	global indexdir, msgdir
	touch(msgdir+hash)
	touch(indexdir+echo)
	open(msgdir+hash, "wb").write(message.encode("utf8"))
	open(indexdir+echo, "a").write(hash+"\n")

def getMsgList(echo):
	global indexdir
	if os.path.exists(indexdir+echo):
		return read_file(indexdir+echo).splitlines()
	else:
		return []

def formatDate(time):
	return datetime.datetime.fromtimestamp(int(time)).strftime("%Y-%m-%d (%A), %H:%M")

def parseTags(str):
	arr=str.split("/")
	tags={}
	for i in range(0,len(arr),2):
		if arr[i+1]:
			tags[arr[i]]=arr[i+1]
	return tags

def check_dirs():
	global indexdir, msgdir
	for directory in [indexdir, msgdir]:
		if not os.path.exists(directory):
			os.makedirs(directory)

def delete(filename, verbose=True):
	if not os.path.exists(filename):
		if verbose:
			print("Файл "+filename+" не существует!")
		return
	try:
		print("rm "+filename)
		os.remove(filename)
	except:
		if verbose:
			print("Ошибка удаления, проверьте права")
