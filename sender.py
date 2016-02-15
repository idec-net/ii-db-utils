#!/usr/bin/env python3
# toss file format is raw msgline, NOT base64

import urllib.parse, urllib.request
import base64, os
from ii_functions import *

authstr="your authstr"
adress="http://ii-net.tk/ii/ii-point.php?q=/"
tossesdir=os.path.join(cwd, "tosses/")

if not os.path.exists(tossesdir):
	os.makedirs(tossesdir)

files=os.listdir(tossesdir)

for file in files:
	f=read_file(tossesdir+file)
	code=b64c(f)
	
	data = urllib.parse.urlencode({'tmsg': code,'pauth': authstr}).encode("utf8")
	out = urllib.request.urlopen(adress + 'u/point', data).read()
	print(out)

	if out.startswith(b'msg ok'):
		delete(tossesdir+file)
