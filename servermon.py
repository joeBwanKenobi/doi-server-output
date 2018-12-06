import sys
import re
import datetime
import urllib.request
import ast
import subprocess
import pty
import os

connections = {}
# class IterUser(type):
# 	def __iter__(cls):
# 		return iter(cls.instances)

class User(object):
	"""
	 The Connection class will be used to create and update a players
	 status during their time on the server.
	"""
	# instances = []
	# count = 0
	def __init__(self, c_date="", c_time="", steam_id="", uname="", ip="", team_cur=""):
		self.steam_id = steam_id
		self.uname = uname
		self.ip = ip
		self.team = team_cur
		self.c_date = c_date
		self.c_time = c_time
		# self.instances.append(self)
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
		# c = 
		c_date, c_time, steam_id, uname, ip = parse_date(line), parse_time(line), parse_steamid(line),\
														parse_uname(line), parse_ip(line)
		return cls(c_date, c_time, steam_id, uname, ip)



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
		steamid = parse_steamid(line)
		connections[steamid] = User.from_string(line)
		for key,val in connections[steamid].__dict__.items():
			print(key, ":", val)
		print()

	elif 'disconnected' in line:
		print('Handling Disconnection Line')
		print(line)

	elif 'joined' in line:
		print('Handling Joined Line')
		print(line)

	elif 'killed' in line:
		print('Handling Killed Line')
		steamid = parse_steamid(line)
		steamid_2 = parse_steamid_2(line)
		connections[steamid].kills += 1
		connections[steamid_2].deaths += 1
		# print("{} just killed {}, {}:{} has {} kills and {} deaths."\
		# 		.format(connections[steamid].uname, connections[steamid_2].uname, \
		# 		connections[steamid].uname, connections[steamid].steamid) \
		# 		str(connections[steamid].kills), str(connections[steamid].deaths))
		# print("------------------>{}:{} has {} kills and {} deaths."\
		# 		.format(connections[steamid_2].uname, connections[steamid_2].steamid, \
		# 		str(connections[steamid_2].kills), str(connections[steamid_2].deaths)))
		print("{} just killed {}, {}:{} has {} kills and {} deaths."\
				.format(connections[steamid].uname, connections[steamid].steamid))
		print("------------------>{}:{} has been killed by {}:{}."\
				.format(connections[steamid_2].uname, connections[steamid_2].steamid, \
				connections[steamid].uname, connections[steamid].steamid))

	elif ' say' in line:
		print('Handling Global Say Line')
		print(line)

	elif 'say_team' in line:
		print('Handling Global Say Line')
		print(line)

	elif 'triggered' in line:
		print('Handling Triggered / Win Line')
		print(line)

	else:
		print('--------->  No Action Words found in line.')
		print(line)

def parse_steamid(line):
	steam_id_pattern = re.compile(r'(STEAM_\d:\d:\d+)')
	steamid = steam_id_pattern.search(line).group(1)
	return steamid

def parse_steamid_2(line):
	steam_id_pattern = re.compile(r'(STEAM_\d:\d:\d+)')
	steamid2 = steam_id_pattern.search(line)
	return steamid2.group(2)

def parse_uname(line):
	uname_pattern = re.compile(r'"([\w\s]+)')
	uname = uname_pattern.search(line).group()
	return uname

def parse_ip(line):
	ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
	ip = ip_pattern.search(line).group()
	return ip

def parse_date(line):
	date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
	date = date_pattern.search(line).group()
	return date

def parse_time(line):
	time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
	time = time_pattern.search(line).group()
	return time

def parse_coords(line):
	coords_pattern = re.compile(r'(-?\d+\.\d+),\s(-?\d+\.\d+),\s(-?\d+\.\d+)')
	coords = coords_pattern.search(line).group()
	return coords

def parse_team_1(line):
	team_1_pattern = re.compile(r'(<#)(\w{2,15})')
	team = team_1_pattern.search(line).group(2)
	return team

def parse_team_2(line):
	team_2_pattern = re.compile(r'("#)(\w{2,15})')
	team = team_2_pattern.search(line).group(2)
	return team
	
def main():
	''' Open a pseudo terminal(pty) to run doi.sh script, output is buffered if piped so a pty is 
	required for real time srcds output
	'''
	
	cmd = ['./doi.sh' ]
	master, slave = pty.openpty()
	p = subprocess.Popen(cmd, shell=True, stdin=slave, stdout=slave, stderr=slave, close_fds=True)
	stdout = os.fdopen(master)
	f = open("output.txt", "w")
	try:
		for line in stdout:
			handle_line(line)
			f.write(line)
	except KeyboardInterrupt:
		print("Keyboard Interrupt --> Exiting writing to logfile and exiting program....")

def from_file():
	log_file = 'testlog1.txt'
	file = open('logs/{}'.format(log_file), 'r')
	try:
		for line in file:
			handle_line(line)
	except KeyboardInterrupt:
		print("Keyboard Interrupt --> Exiting writing to logfile and exiting program....")


''' Print Connection object instances '''
# for c in Connection:
# 	print(c)

if __name__ == "__main__":
	from_file()