#!/usr/bin/env python3
# forked from spline1986's versions

import sys, sqlite3
from ii_functions import *

args=sys.argv[1:]

if len(args)==0:
	print("Usage: sqlite-import.py <db_file>")
	sys.exit(1)

check_dirs()

conn = sqlite3.connect(args[0])
c = conn.cursor()

echoareas = []
for row in c.execute("SELECT echoarea FROM msg GROUP BY echoarea;"):
	echoareas.append(row[0])

for echoarea in echoareas:
	print("Echoarea: " + echoarea)

	if echoarea=="":
		continue

	echo = open(indexdir + echoarea, "wb")
	msgids = []
	for msg in c.execute("SELECT * FROM msg WHERE echoarea = '" + echoarea + "' ORDER BY id;"):
		print("MSGID: " + msg[1])
		echo.write(msg[1] + "\n")
		msgf = open(msgdir + msg[1], "wb")
		rawtext = msg[2] + "\n" + msg[3] + "\n" + str(msg[4]) + "\n" + msg[5] + "\n" + msg[6] + "\n" + msg[7] + "\n" + msg[8] + "\n\n" + msg[9]
		msgf.write(rawtext.encode("utf8"))
		msgf.close()
		print("OK")
	echo.close()

conn.close()
