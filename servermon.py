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
	

	if ' connected' in line:
		print('Handling Connection Line')
		parseInfo(line)
		print(line)
	elif 'disconnected' in line:
		print('Handling Disconnection Line')
		parseInfo(line)
		print(line)
	elif 'joined' in line:
		print('Handling Joined Line')
		parseInfo(line)
		print(line)
	elif 'killed' in line:
		print('Handling Killed Line')
		parseInfo(line)
		print(line)
	elif ' say' in line:
		print('Handling Global Say Line')
		parseInfo(line)
		print(line)
	elif 'say_team' in line:
		print('Handling Global Say Line')
		parseInfo(line)
		print(line)
	elif 'triggered' in line:
		print('Handling Triggered / Win Line')
		parseInfo(line)
		print(line)
	else:
		print('No Action Words found in line.')
		# parseInfo(line)
		# print(line)


def parseInfo(line):
	"""
	Parses incoming strings from DOI Source Server, decides if the
	string should be returned to create a connection object, update
	an existing connection, update the server status, or output to 
	console.
	"""
	ip = ""
	date = ""
	time = ""
	uname = ""
	steamID = ""
	coords = ""
	weapon = ""
	message = ""
	team_cur = ""
	team_new = ""
	team_join = ""
	connect_time = ""
	disconnect_time = ""

	"""
	Set patterns to search for
	date: mm/dd/yyyy
	time: hr:mm:ss
	"""
	ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}')
	date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
	time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
	uname_pattern = re.compile(r'"([\w\s]+)')
	steamID_pattern = re.compile(r'STEAM_\d:\d:\d+')
	coords_pattern = re.compile(r'(-?\d+\.\d+),\s(-?\d+\.\d+),\s(-?\d+\.\d+)')
	team_cur_pattern = re.compile(r'(<#)(\w{2,15})')
	team_join_pattern = re.compile(r'("#)(\w{2,15})')

	"""
	If patterns are NoneType, pass, otherwise assign to variable
	"""
	if ip_pattern.search(line) is not None:
		ip = ip_pattern.search(line).group()

	if date_pattern.search(line).group() is not None:
		date = date_pattern.search(line).group()
	
	if time_pattern.search(line).group() is not None:
		time = time_pattern.search(line).group()
	
	if uname_pattern.search(line) is not None:
		uname = uname_pattern.search(line).group(1)

	if steamID_pattern.search(line) is not None:
		steamID = steamID_pattern.search(line).group()

	if coords_pattern.search(line) is not None:
		coords = coords_pattern.search(line).group()

	if team_cur_pattern.search(line) is not None:
		team_curr = team_cur_pattern.search(line).group(2)

	if team_join_pattern.search(line) is not None:
		team_join = team_join_pattern.search(line).group(2)

	
	return print('\x1b[6;30;42m' + date, time, uname, ip, steamID, coords, team_cur, team_join + '\x1b[0m')

for line in sys.stdin:
	# parseInfo(line)
	handleLine(line)
