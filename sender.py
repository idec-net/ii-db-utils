#!/usr/bin/env python2
# -*- coding:utf8 -*-
# toss file format is raw msgline, NOT base64

import urllib,base64,os

authstr="your authstr"
adress="http://ii-net.tk/ii/ii-point.php?q=/"
tossesdir="tosses/"

files=os.listdir(tossesdir)

for file in files:
	f=open(tossesdir+file).read()
	code=base64.b64encode(f)
	
	data = urllib.urlencode({'tmsg': code,'pauth': authstr})
	out = urllib.urlopen(adress + 'u/point', data).read()
	print out

	if out.startswith('msg ok'):
		os.remove(tossesdir+file)
