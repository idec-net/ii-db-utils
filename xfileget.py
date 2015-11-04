#!/usr/bin/python3

import urllib.parse, urllib.request, sys, math

authstr="your_authstr"
station="http://your-station.ru/"

argv=sys.argv[1:]
argc=len(argv)

def prettier_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
	r,f=min(int(math.log(max(n*b**pow,1),b)),len(pre)-1),'{:,.%if} %s%s'
	return (f%(abs(r%(-r-1)),pre[r],u)).format(n*b**pow/b**float(r))

if argc>0:
	data = urllib.parse.urlencode({'pauth': authstr, 'filename':argv[0]}).encode('utf8')
	out = urllib.request.urlopen(station + 'x/file', data)
	
	file_size=0
	block_size=8192
	
	f=open(argv[0], "wb")
	while True:
		buffer=out.read(block_size)
		if not buffer:
			break
		file_size+=len(buffer)
		f.write(buffer)
	f.close()
	print("Скачали "+str(prettier_size(file_size)))

else:
	data = urllib.parse.urlencode({'pauth': authstr}).encode('utf8')
	files = urllib.request.urlopen(station + 'x/file', data).read().splitlines()
	for file in files:
		a=file.decode("utf8").split(":")

		if (len(a)<3):
			print(file)
		else:
			print(a[0]+" | "+prettier_size(int(a[1]))+" | "+a[2])
