import sys
import re
import datetime

class Connection:
	"""
	 The Connection class will be used to create and update a players
	 status during their time on the server.
	"""
	def __init__(self, steamID, uname, IP, team, connect_time, disconnect_time):
		self.steamID = steamID
		self.uname = uname
		self.IP = IP
		self.team = team
		self.connect_time = connect_time
		self.disconnect_time = disconnect_time

def parseInfo(line):
	"""
	Parses incoming strings from DOI Source Server, decides if the
	string should be returned to create a connection object, update
	an existing connection, update the server status, or output to 
	console.
	"""
	date = ""
	time = ""
	name = ""
	"""
	Set patterns to search for
	date: mm/dd/yyyy
	time: hr:mm:ss


	"""
	date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
	time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
	name_pattern = re.compile(r'"([\w\s]+)')

	"""
	If patterns are NoneType, pass, else assign to variable
	"""
	if date_pattern.search(line).group() is not None:
		date = date_pattern.search(line).group()
	else:
		pass
	if time_pattern.search(line).group() is not None:
		time = time_pattern.search(line).group()
	else:
		pass
	if name_pattern.search(line) is not None:
		name = name_pattern.search(line).group(1)
	else:
		pass
	return print(date, time, name)

for line in sys.stdin:
	parseInfo(line)
