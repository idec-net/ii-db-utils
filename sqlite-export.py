#!/usr/bin/env python2
# forked from spline1986's versions

import os, sys, sqlite3
from ii_functions import *

args=sys.argv[1:]

if(len(args)==0):
	print "Usage: sqlite-export.py <db_file>"
	sys.exit(1)

conn = sqlite3.connect(args[0])
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS msg(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
msgid TEXT,
kludges TEXT,
echoarea TEXT,
timestump INTEGER,
from_name TEXT,
address TEXT,
to_name TEXT,
subject TEXT,
body TEXT,
UNIQUE (id, msgid));""")

echoareas = sorted(os.listdir("echo/"))

for echoarea in echoareas:
	print "Echoarea: " + echoarea
	msgids = getMsgList(echoarea)
	for msgid in msgids[:-1]:
		print "MSGID: " + msgid
		msg = getMsg(msgid)
		c.execute("INSERT OR IGNORE INTO msg (msgid, kludges, echoarea, timestump, from_name, address, to_name, subject, body) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (msgid, "/".join(msg["tags"]), msg["echo"], msg["time"], msg["sender"], msg["addr"], msg["to"], msg["subj"], msg["msg"]))
		print "OK"
	conn.commit()

conn.close()
