#!/usr/bin/env python2
# -*- coding:utf8 -*-

rawletters="new/" # new raw messages to parse them
indexdir="echo/"
messagesdir="msg/"

echo="mailbox.14"
addr="mscript, 1"
tags="ii/ok"

from email.utils import parsedate,parseaddr
from email.Header import decode_header
import email.parser as pars
import os
import time
import base64
import hashlib
import html2text

def hsh(str):
	return base64.urlsafe_b64encode( hashlib.sha256(str).digest() ).replace('-','A').replace('_','z')[:20]

myparser=pars.Parser()
h = html2text.HTML2Text()
h.ignore_links = True

for filename in os.listdir(rawletters):
	letterpath=os.path.join(rawletters, filename)
	
	plainmessage=open(letterpath).read()
	message=myparser.parsestr(plainmessage)
	
	msgdate=0
	sender="nobody"
	to="All"
	subj="..."
	msg="no message"
	
	if(message['date']):
		parsdate=parsedate(message['date'])
		msgdate=int(time.mktime(parsdate))

	if(message['from']):
		sender=parseaddr(message['from'])[1]
	
	if(message['to']):
		to=parseaddr(message['to'])[1]
	
	if(message['subject']):
		decodefrag = decode_header(message['subject'])
		subj_fragments = []
		for s , enc in decodefrag:
			if enc:
				s = unicode(s , enc).encode('utf8','replace')
			subj_fragments.append(s)
		subj = ''.join(subj_fragments)
	
	if(message.is_multipart()):
		for part in message.walk():
			charset=message.get_content_charset()
			if(not charset):
				charset='ascii'
			payload=part.get_payload(decode=True)
			if(not payload):
				continue
			msg+="\n"+h.handle(payload.decode("utf8")).strip().replace("\n\n","\n")
	else:
		# charset=message.get_content_charset() or "ascii"
		msg=h.handle(message.get_payload(decode=True).decode("utf8")).strip().replace("\n\n", "\n")
		
	iimsg=tags+"\n"+echo+"\n"+str(msgdate)+"\n"+sender+"\n"+addr+"\n"+to+"\n"+subj+"\n"
	iimsg+="\n"+msg.encode("utf8")

	msgid=hsh(iimsg)
	open(os.path.join(messagesdir, msgid), "w").write(iimsg)
	open(os.path.join(indexdir, echo), "a").write(msgid+"\n")
	os.remove(letterpath)
