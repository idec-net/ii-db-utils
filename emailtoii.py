#!/usr/bin/env python3

echo="mailbox.15"
addr="mscript, 1"
tags="ii/ok"

from email.utils import parsedate, parseaddr
from email.header import decode_header
import email.parser as pars
import os
import time
import html2text

from ii_functions import *

check_dirs()

rawletters=os.path.join(cwd, "new/") # new raw messages to parse them

myparser=pars.BytesParser()

h = html2text.HTML2Text()
h.ignore_links = True

for filename in os.listdir(rawletters):
	letterpath=os.path.join(rawletters, filename)
	
	plainmessage=open(letterpath, "rb").read()
	message=myparser.parsebytes(plainmessage)
	
	msgdate=0
	sender="nobody"
	to="All"
	subj="..."
	msg="no message"
	
	if message['date']:
		parsdate=parsedate(message['date'])
		msgdate=int(time.mktime(parsdate))

	if message['from']:
		sender=parseaddr(message['from'])[1]

	if message['to']:
		to=parseaddr(message['to'])[1]

	if message['subject']:
		parts=decode_header(message['subject'])[0]
		subj=parts[0]
		charset=parts[1]
		if charset:
			subj=subj.decode(charset)

	if message.is_multipart():
		for part in message.walk():
			charset=part.get_content_charset() or 'ascii'
			payload=part.get_payload(decode=True)
			if not payload:
				continue
			try:
				payload=payload.decode(charset)
				msg+="\n"+h.handle(payload).strip().replace("\n\n","\n")
			except:
				msg+="can't decode\n"
	else:
		charset=message.get_content_charset() or "ascii"
		msg=h.handle(message.get_payload(decode=True).decode(charset)).strip().replace("\n\n", "\n")

	iimsg=tags+"\n"+echo+"\n"+str(msgdate)+"\n"+str(sender)+"\n"+str(addr)+"\n"+str(to)+"\n"+str(subj)+"\n"
	iimsg+="\n"+msg

	msgid=hsh(iimsg)
	savemsg(msgid, echo, iimsg)
	delete(letterpath)
