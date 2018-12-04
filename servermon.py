import sys
import re
import datetime
import urllib.request
import ast
import subprocess
import pty
import os

class IterConnection(type):
	def __iter__(cls):
		return iter(cls.instances)

class Connection(metaclass=IterConnection):
	"""
	 The Connection class will be used to create and update a players
	 status during their time on the server.
	"""
	instances = []
	count = 0

	def __init__(self, c_date, c_time, steam_id, uname, ip, team_cur=None):
		self.steam_id = steam_id
		self.uname = uname
		self.ip = ip
		self.team = team_cur
		self.c_date = c_date
		self.c_time = c_time
		self.instances.append(self)
		"""
		Need to implement hashfile to store ip's and loc info to save 
		get_ip() calls
		"""
		self.location = self.get_location(ip)

	def get_location(self, ip):
		with urllib.request.urlopen('https://ipinfo.io/{}'.format(self.ip)) as response:
			loc = ast.literal_eval(response.read().decode('UTF-8'))
		return loc

	@property
	def description(self):
		return "> {}-{} --> connection from address: {}\n{} {}\n{}, {}, {}\n{}".format(\
			self.c_date, self.c_time, self.ip, self.uname, self.steam_id, self.location['city'], \
			self.location['region'], self.location['country'], self.location['org'])

	@classmethod
	def from_string(cls, line):
		c = parse_info(line)
		c_date, c_time, steam_id, uname, ip, team_cur = c[0], c[1], c[2], c[3], \
		c[4], c[5]
		return cls(c_date, c_time, steam_id, uname, ip, team_cur)



def handle_line(line):
	"""
	Decides what to do with incoming data based on words in line,
	connected, = create connection object
	disconnected = destroy connection object, save to log file
	killed = display line, update kills and deaths for connection objects
	joined = display team change line, update server / team data
	"""
	

	if ' connected,' in line:
		# print('Handling Connection Line')
		c1 = Connection.from_string(line)
		print(c1.description)
	elif 'disconnected' in line:
		print('Handling Disconnection Line')
		parse_info(line)
		print(line)
	elif 'joined' in line:
		print('Handling Joined Line')
		parse_info(line)
		print(line)
	elif 'killed' in line:
		print('Handling Killed Line')
		parse_info(line)
		print(line)
	elif ' say' in line:
		print('Handling Global Say Line')
		parse_info(line)
		print(line)
	elif 'say_team' in line:
		print('Handling Global Say Line')
		parse_info(line)
		print(line)
	elif 'triggered' in line:
		print('Handling Triggered / Win Line')
		parse_info(line)
		print(line)
	else:
		print('--------->  No Action Words found in line.')
		# parse_info(line)
		print(line)


def parse_info(line):
	# import pdb; pdb.set_trace()
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

	"""Set patterns to search for"""

	'''Find IPv4 address by searching for 3 groups of [0-9]. followed by one group of 3 [0-9] separated by whitespace on both sides
	   this prevents assigning the first coordinate to ip variable'''
	ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
	date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
	time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
	uname_pattern = re.compile(r'"([\w\s]+)')
	steam_id_pattern = re.compile(r'STEAM_\d:\d:\d+')
	coords_pattern = re.compile(r'(-?\d+\.\d+),\s(-?\d+\.\d+),\s(-?\d+\.\d+)')
	team_cur_pattern = re.compile(r'(<#)(\w{2,15})')
	team_join_pattern = re.compile(r'("#)(\w{2,15})')

	"""If patterns are NoneType, pass, otherwise assign to variable"""
	if ip_pattern.search(line) is not None:
		ip = ip_pattern.search(line).group()
		print("IP ASSIGNED: {}".format(ip))

	if date_pattern.search(line) is not None:
		date = date_pattern.search(line).group()
		print("DATE ASSIGNED: {}".format(date))
	
	if time_pattern.search(line) is not None:
		time = time_pattern.search(line).group()
		print("TIME ASSIGNED: {}".format(time))
	
	if uname_pattern.search(line) is not None:
		uname = uname_pattern.search(line).group(1)
		print("UNAME ASSIGNED: {}".format(uname))

	if steam_id_pattern.search(line) is not None:
		steam_id = steam_id_pattern.search(line).group()
		print("STEAMID ASSIGNED: {}".format(steam_id))
	if coords_pattern.search(line) is not None:
		coords = coords_pattern.search(line).group()
		print("COORDS ASSIGNED: {}".format(coords))

	if team_cur_pattern.search(line) is not None:
		team_curr = team_cur_pattern.search(line).group(2)
		print("TEAM_CURR ASSIGNED: {}".format(team_curr))

	if team_join_pattern.search(line) is not None:
		team_join = team_join_pattern.search(line).group(2)
		print("TEAM_JOIN ASSIGNED: {}".format(team_join))

	
	# print('\x1b[6;30;42m' + date, time, uname, ip, steam_id, coords, team_cur, team_join + '\x1b[0m')
	return date, time, steam_id, uname, ip, team_cur, team_join, coords



''' Print Connection object instances '''
# for c in Connection:
# 	print(c)

''' Open a pseudo terminal(pty) to run doi.sh script, output is buffered if piped
	so a pty is required for real time srcds output
'''

# pdb.set_trace()
# cmd = ['./doi.sh' ]
# master, slave = pty.openpty()
# p = subprocess.Popen(cmd, shell=True, stdin=slave, stdout=slave, stderr=slave, close_fds=True)
# stdout = os.fdopen(master)
# f = open("output.txt", "w")
# try:
# 	for line in stdout:
# 		handle_line(line)
# 		f.write(line)
# except KeyboardInterrupt:
# 	print("Keyboard Interrupt --> Exiting writing to logfile and exiting program....")


file = open('logs/less-info.txt', 'r')
try:
	for line in file:
		handle_line(line)
except KeyboardInterrupt:
	print("Keyboard Interrupt --> Exiting writing to logfile and exiting program....")