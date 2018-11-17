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


def handleLine(line):
	"""
	Decides what to do with incoming data based on words in line,
	connected = create connection object
	disconnected = destroy connection object, save to log file
	killed = display line, update kills and deaths for connection objects
	joined = display team change line, update server / team data
	"""
	action_w = ""
	find_words = ['connected','disconnected','joined','killed']
	connected = re.compile(r'\sconnected')



	if ' connected' in line:
		print('Handling Connection Line')
		print(line)
	elif 'disconnected' in line:
		print('Handling Disconnection Line')
		print(line)
	elif 'joined' in line:
		print('Handling Joined Line')
		print(line)
	elif 'killed' in line:
		print('Handling Killed Line')
		print(line)
	else:
		print('No Action Words found in line.')
		print(line)


def parseInfo(line):
	"""
	Parses incoming strings from DOI Source Server, decides if the
	string should be returned to create a connection object, update
	an existing connection, update the server status, or output to 
	console.
	"""
	date = ""
	time = ""
	connect_time = ""
	disconnect_time = ""
	uname = ""
	steamID = ""

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
	# parseInfo(line)
	handleLine(line)
