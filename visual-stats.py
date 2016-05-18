#!/usr/bin/env python3

import sys, calendar, datetime
from ii_functions import *

def parse_date(string):
	date=string.split(".")
	date=[int(x) for x in date]
	return calendar.timegm(datetime.date(date[0], date[1], date[2]).timetuple())

def usage_quit():
	print("Usage: visual-stats.py -t [stats_type] -s YYYY.MM.DD -e YYYY.MM.DD.\n\
stats_type must be \"echoareas\" or \"points\"\n")
	sys.exit(1)

def calculate_stat(echoareas, stat_type="echoareas"):
	stat = {}
	ret = []
	for echoarea in echoareas:
		msgids = getMsgList(echoarea)
		for msgid in msgids:
			if len(msgid) == 20:
				msg = getMsg(msgid)
				msgtime = int(msg["time"])

				if msgtime >= start_date and msgtime < end_date:
					if stat_type == "points":
						item = msg["sender"]
					else:
						item = echoarea

					if not item in stat:
						stat[item] = 1
					else:
						stat[item] += 1
	for item in stat:
		ret.append([item, stat[item]])
	return sorted(ret, key=lambda ret: ret[1], reverse = True)

args=sys.argv[1:]

start_on = "-s" in args
end_on = "-e" in args
type_on = "-t" in args

if len(args) != 6 or not start_on or not end_on or not type_on:
	usage_quit()

start_date = parse_date( args[args.index("-s") + 1] )
end_date   = parse_date( args[args.index("-e") + 1] )
stat_type  = args[args.index("-t") + 1]

echoareas=input("Введите нужные эхи через пробел: ").split(" ")
stat = calculate_stat(echoareas, stat_type)
value_of_division = round(stat[0][1] / 54 + 0.49)

if value_of_division == 0:
	print("There are no messages in these echoareas during this time.\n")
	quit()

if stat_type == "points":
	title = "Users"
else:
	title = "Echoareas"

total = 0
print("\n%-25s ▒ ≈ %s messages" % (title, value_of_division))
print("───────────────────────────────────────────────────────────────────────────────")
for item in stat:
	dots = ""
	graph = ""
	empty = ""
	for i in range(1, 25 - len(item[0]) - len(str(item[1]))):
		dots += "."
	for i in range(1, round(item[1] / value_of_division + 0.49) + 1):
		graph += "█"
	for i in range(1, 55 - len(graph)):
		empty += "▒"
	print("%s%s%s %s%s" % (item[0], dots, item[1], graph, empty))
	total += item[1]
print("───────────────────────────────────────────────────────────────────────────────")

empty = ""
for i in range(1, 20 - len(str(total))):
	empty += " "

print("Total", empty, total, sep="")