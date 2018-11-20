import sys
import re
import datetime
import urllib.request
import ast

class Connection:
	"""
	 The Connection class will be used to create and update a players
	 status during their time on the server.
	"""
	def __init__(self, c_date, c_time, steam_id, uname, ip, team_cur=None):
		self.steam_id = steam_id
		self.uname = uname
		self.ip = ip
		self.team = team_cur
		self.c_date = c_date
		self.c_time = c_time
		"""
		Need to implement hashfile to store ip's and loc info to save 
		get_ip() calls
		"""
		self.location = self.get_location()

	@property
	def description(self):
		return "{} {} {} - {} connection created from address: {}\n {}".format(\
			self.c_date, self.c_time, self.uname, self.steam_id, self.ip, self.location)

	@classmethod
	def from_string(cls, line):
		c = parse_info(line)
		print(c)
		c_date, c_time, steam_id, uname, ip, team_cur = c[0], c[1], c[2], c[3], \
		c[4], c[5]
		return cls(c_date, c_time, steam_id, uname, ip, team_cur)


def get_location(ip):
		print('IP ADDRESS IN get_location(): ' + ip)
		with urllib.request.urlopen('https://ipinfo.io/{}'.format(ip)) as response:
			loc = ast.literal_eval(response.read().decode('UTF-8'))
		return loc


def handle_line(line):
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
		# parse_info(line)
		# print(line)
	elif 'joined' in line:
		pass
		# print('Handling Joined Line')
		# parse_info(line)
		# print(line)
	elif 'killed' in line:
		pass
		# print('Handling Killed Line')
		# parse_info(line)
		# print(line)
	elif ' say' in line:
		pass
		# print('Handling Global Say Line')
		# parse_info(line)
		# print(line)
	elif 'say_team' in line:
		pass
		# print('Handling Global Say Line')
		# parse_info(line)
		# print(line)
	elif 'triggered' in line:
		pass
		# print('Handling Triggered / Win Line')
		# parse_info(line)
		# print(line)
	else:
		print('No Action Words found in line.')
		# parse_info(line)
		# print(line)


def parse_info(line):
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
	steam_id = ""
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
	steam_id_pattern = re.compile(r'STEAM_\d:\d:\d+')
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

	if steam_id_pattern.search(line) is not None:
		steam_id = steam_id_pattern.search(line).group()

	if coords_pattern.search(line) is not None:
		coords = coords_pattern.search(line).group()

	if team_cur_pattern.search(line) is not None:
		team_curr = team_cur_pattern.search(line).group(2)

	if team_join_pattern.search(line) is not None:
		team_join = team_join_pattern.search(line).group(2)

	
	# print('\x1b[6;30;42m' + date, time, uname, ip, steam_id, coords, team_cur, team_join + '\x1b[0m')
	return date, time, steam_id, uname, ip, team_cur, team_join, coords

for line in sys.stdin:
	# parse_info(line)
	handle_line(line)