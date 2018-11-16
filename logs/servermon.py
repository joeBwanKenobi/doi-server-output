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

def parseInfo():
	in_str = sys.stdin.readline()
	print(in_str)
	print()
	date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
	time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
	name_pattern = re.compile(r'"([a-zA-Z0-9]+)(\s[a-zA-Z0-9]+)?')


	date = date_pattern.search(in_str).group()
	time = time_pattern.search(in_str).group()
	name = name_pattern.search(in_str).groups()
	print(date, time, name)

pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
text_to_search = '''
09/24/2018 - 12:21:57: "mion<555><STEAM_1:1:61086992><#nva>" disconnected (reason "Disconnected.")
'''
matches = pattern.search(text_to_search)


# for match in matches:
# 	print(match)

# print(matches.group(0))
for line in sys.stdin:
	parseInfo()