import sys
import re
import datetime

class Connection:
	"""
	 The Connection class will be used to create and update a players
	 status during their time on the server.
	"""
	def __init__(self, c_date, c_time, steamID, uname, ip, team_cur=None):
		self.steamID = steamID
		self.uname = uname
		self.ip = ip
		self.team = team_cur
		self.c_date = c_date
		self.c_time = c_time

	@property
	def description(self):
		return "{} {} {} - {} connection created from address: {}".format(\
			self.c_date, self.c_time, self.uname, self.steamID, self.ip)

	@classmethod
	def from_string(cls, line):
		c = parseInfo(line)
		print(c)
		c_date, c_time, steamID, uname, ip, team_cur = c[0], c[1], c[2], c[3], \
		c[4], c[5]
		return cls(c_date, c_time, steamID, ip, team_cur)

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
		c1 = Connection.from_string(line)
		print(c1.description)
		
	elif 'disconnected' in line:
		pass
		# print('Handling Disconnection Line')
		# parseInfo(line)
		# print(line)
	elif 'joined' in line:
		pass
		# print('Handling Joined Line')
		# parseInfo(line)
		# print(line)
	elif 'killed' in line:
		pass
		# print('Handling Killed Line')
		# parseInfo(line)
		# print(line)
	elif ' say' in line:
		pass
		# print('Handling Global Say Line')
		# parseInfo(line)
		# print(line)
	elif 'say_team' in line:
		pass
		# print('Handling Global Say Line')
		# parseInfo(line)
		# print(line)
	elif 'triggered' in line:
		pass
		# print('Handling Triggered / Win Line')
		# parseInfo(line)
		# print(line)
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

	
	# print('\x1b[6;30;42m' + date, time, uname, ip, steamID, coords, team_cur, team_join + '\x1b[0m')
	return date, time, steamID, uname, ip, team_cur, team_join, coords

for line in sys.stdin:
	# parseInfo(line)
	handleLine(line)