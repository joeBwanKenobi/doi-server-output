#!/usr/bin/env python3
import sys
import re
import datetime
import urllib.request
import ast
import subprocess
import pty
import os

connections = {}
stored_ips = {}
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
	def __init__(self, c_date="", c_time="", steam_id="", uname="", ip="", team=""):
		self.steam_id = steam_id
		self.uname = uname
		self.ip = ip
		self.team = team
		self.c_date = c_date
		self.c_time = c_time
		self.kills = 0
		self.deaths = 0
		# self.instances.append(self)
		"""
		Need to implement hashfile to store ip's and loc info to save 
		get_ip() calls
		"""
		self.location = self.get_location(ip)

	def get_location(self, ip):
		with urllib.request.urlopen('https://ipinfo.io/{}'.format(self.ip)) as response:
		 	loc = ast.literal_eval(response.read().decode('UTF-8'))
		# loc = "TEST LOCATION"
		return loc

	@property
	def description(self):
		return print("{}-{}-->  connection from address: {}\n\t\t\t{} {}\n\t\t\t{}, {}, {}\n\t\t\t{}\n".format(\
			self.c_date, self.c_time, self.ip, self.uname, self.steam_id, self.location['city'], \
			self.location['region'], self.location['country'], self.location['org']))

	@classmethod
	def from_string(cls, line):
		# c = 
		c_date, c_time, steam_id, uname, ip = parse_date(line), parse_time(line), parse_steamid(line)[0],\
														parse_uname(line), parse_ip(line)
		return cls(c_date, c_time, steam_id, uname, ip)

	@classmethod
	def bot_from_string(cls, line):
		# c = 
		c_date, c_time, steam_id, uname = parse_date(line), parse_time(line), parse_bot_id(line)[0],\
														parse_uname(line)
		return cls(c_date, c_time, steam_id, uname)



def handle_line(line):
	"""
	Decides what to do with incoming data based on words in line,
	connected, = create connection object
	disconnected = destroy connection object, save to log file
	killed = display line, update kills and deaths for connection objects
	joined = display team change line, update server / team data
	"""
	
	if ' connected,' in line:
		if '<BOT>' in line:
			steamid = parse_bot_id(line)[0]
			connections[steamid] = User.bot_from_string(line)
			connections[steamid].description
			# for key,val in connections[steamid].__dict__.items():
			# 	print(key, ":", val)
		else:
			steamid = parse_steamid(line)[0]
			connections[steamid] = User.from_string(line)
			connections[steamid].description
			# for key,val in connections[steamid].__dict__.items():
			# 	print(key, ":", val)

	elif 'disconnected' in line:
		print('Handling Disconnection Line')
		print(line)

	elif 'joined' in line:
		if 'BOT' in line:
			steamid = parse_bot_id(line)[0]
			team = parse_team(line)
			connections[steamid].team = team[1]
			print("{}-{}--> Player: {}({}): joined team {}\n".format(parse_time(line), parse_date(line), \
															connections[steamid].uname, team[0], team[1]))
		else:
			steamid = parse_steamid(line)[0]
			team = parse_team(line)
			connections[steamid].team = team[1]
			print("{}-{}--> Player: {}({}): joined team {}\n".format(parse_time(line), parse_date(line), \
															connections[steamid].uname, team[0], team[1]))

	elif ' killed ' in line:
		if '<BOT>' in line and not parse_steamid(line):  # Only bots in line, bot on bot crime
			bot_id_list = parse_bot_id(line)
			steamid, steamid_2 = bot_id_list[0], bot_id_list[1]
		elif '<BOT>' in line:
			steamid = parse_steamid(line)[0] if is_first(line) else parse_bot_id(line)[0]  # Player with SteamID in first position, killed bot
			steamid_2 = parse_bot_id(line)[0] if is_first(line) else parse_steamid(line)[0]  # Bot in first position, killed Player with SteamID
		else:
			steamid_list = parse_steamid(line)
			steamid = steamid_list[0]
			steamid_2 = steamid_list[1]

		'''If all Steam IDs in kill exist as objects in connections{} then increase kill 
		count for steamid and death count for steamid_2 
		'''
		if all (ids in connections for ids in (steamid, steamid_2)):
			connections[steamid].kills += 1
			connections[steamid_2].deaths += 1
			print("{}-{}--> {}: K:{} D:{} just killed {}: K:{} D:{}\n"\
				.format(parse_date(line), parse_time(line),connections[steamid].uname, \
				connections[steamid].kills, connections[steamid].deaths,\
				 connections[steamid_2].uname, connections[steamid_2].kills, connections[steamid_2].deaths))
			print()
		else:
			print("A STEAM ID DOESN'T EXIST IN connections")
	
	elif ' say ' in line:
		steamid = parse_steamid(line)[0]
		print('{}-{}--> {}: {}'.format(parse_date(line), parse_time(line), connections[steamid].uname, parse_message(line)))
		print()

	elif 'say_team' in line:
		steamid = parse_steamid(line)[0]
		print('{}-{}--> {}({}): {}\n'.format(parse_date(line), parse_time(line), connections[steamid].uname,\
		 							connections[steamid].team, parse_message(line)))
		print()

	elif 'triggered' in line:
		if 'obj_captured' and 'Team' in line:
			team = parse_team(line)[0]
			print("{}-{}--> {} captured a point.\n".format(parse_date(line), parse_time(line), team.upper()))
		elif parse_steamid(line) or parse_bot_id(line):
			steamid = parse_steamid(line)[0] if parse_steamid(line) else parse_bot_id(line)[0]
			team = parse_team(line)[0]
			print("{}-{}--> {}({}): captured a point.\n".format(parse_date(line), parse_time(line), \
														connections[steamid].uname, team))
		elif 'Round_Win' in line:
			team = parse_team(line)[0]
			print("{}-{}--> {} has won the round!\n".format(parse_date(line), parse_time(line), team.upper()))


def parse_steamid(line):
	'''Returns list of Steam ID's found in line'''
	steam_id_pattern = re.compile(r'(STEAM_\d:\d:\d+)')
	steamid = steam_id_pattern.findall(line)
	if not steamid:
		return False
	else:
		return steamid

# def parse_steamid_2(line):
# 	'''Retruns second Steam ID found in line'''
# 	steam_id_pattern = re.compile(r'(STEAM_\d:\d:\d+)')
# 	steamid = steam_id_pattern.findall(line)
# 	return steamid[1]

def parse_bot_id(line):
	'''Returns list of BotID's from line'''
	bot_id_pattern = re.compile(r'<(\d+)><(\w+)>')
	botid = bot_id_pattern.findall(line)
	if len(botid) > 1:
		botid = [botid[0][0] + botid[0][1], botid[1][0] + botid[1][1]]
		return botid
	else:
		botid = [botid[0][0] + botid[0][1]]
		return botid

def parse_uname(line):
	'''Retrun username from line'''
	uname_pattern = re.compile(r'"([\w\s]+)')
	uname = uname_pattern.search(line).group(1)
	return uname

def parse_ip(line):
	'''Return IPv4 address from line'''
	ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
	ip = ip_pattern.search(line).group()
	return ip

def parse_date(line):
	'''Return date from line'''
	date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
	date = date_pattern.search(line).group()
	return date

def parse_time(line):
	'''Return time from line'''
	time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
	time = time_pattern.search(line).group()
	return time

def parse_coords(line):
	'''Retrun coordinates found in line'''
	coords_pattern = re.compile(r'(-?\d+\.\d+),\s(-?\d+\.\d+),\s(-?\d+\.\d+)')
	coords = coords_pattern.search(line).group()
	return coords

def parse_team(line):
	'''Returns list of teams found in line'''
	team_pattern = re.compile(r'#(\w{1,15})')
	team = team_pattern.findall(line)
	return team

# def parse_team_2(line):
# 	'''Return second team in line'''
# 	team_2_pattern = re.compile(r'("#)(\w{2,15})')
# 	team = team_2_pattern.search(line).group(2)
	# return team

def parse_message(line):
	'''Return user chat input'''
	msg_pattern = re.compile(r'"(.*?)"')
	return msg_pattern.findall(line)[1]

def is_first(line):
	steam_id_pattern = re.compile(r'(STEAM_\d:\d:\d+)')
	bot_id_pattern = re.compile(r'<(\d+)><(\w+)>')

	if steam_id_pattern.search(line):
		'''Returns 1 if Steam ID shows up before BOT ID in line'''
		for j in steam_id_pattern.finditer(line):
			x = j.start()

		for i in bot_id_pattern.finditer(line):
			y = i.start()

		if x < y:
			return 1
		else:
			return 0


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
		print("Keyboard Interrupt --> Exiting writing to logfile and exiting program....\n")

def from_file():
	log_file = 'error-log-stripped'
	file = open('logs/{}.txt'.format(log_file), 'r')
	try:
		for line in file:
			handle_line(line)
	except KeyboardInterrupt:
		print("Keyboard Interrupt --> Exiting writing to logfile and exiting program....\n")
	for key in connections:
		print(connections.get(key).__dict__.items())
		# for k,v in connections[key].__dict__.items():
		# 	print(k, ":", v)


''' Print Connection object instances '''
# for c in Connection:
# 	print(c)

if __name__ == "__main__":
	from_file()