import sys
import re
import datetime

class Connection:

	def __init__(self, steamID, uname, IP, team, connect_time, disconnect_time):
		self.steamID = steamID
		self.uname = uname
		self.IP = IP
		self.team = team
		self.connect_time = connect_time
		self.disconnect_time = disconnect_time

def parseInfo(line):
	date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
	time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
	name_pattern = re.compile(r'"([\w\s]+)')


	date = date_pattern.search(line).group()
	time = time_pattern.search(line).group()
	name = name_pattern.search(line).group(1)
	return print(date, time, name)

for line in sys.stdin:
	# print()
	# print(line)
	parseInfo(line)
