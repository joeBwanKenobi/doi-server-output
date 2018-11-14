#!/bin/bash
# servermon.sh is a script that parses, cleans up, and displays data from the output of a Source Enginge Server
# Supported Servers: Day of Infamy

# Setting global color variables for printing
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
ORANGE='\033[0;33m'
PURPLE='\033[0;35m'
GRAY='\033[0;37m'
NC='\033[0m' # No color

# Takes input $IP from main function and geolocates it via ipinfo.io.
# !!!FIX!!! Still adds cities / countries with spaces in name to multiple indeces even though wrapped in quotes
locate_ip()
{
	IP=$1
	# Pull location information from ipinfo.io
	rawipinfo=`curl -s ipinfo.io/$IP`
	declare -a list=(`echo "${rawipinfo//[:,\{\}]/}"`);
	# Print out array for debugging
	#echo -e "${list[@]}\n"
	# Loop through IP information to match "city" "region" "country"
	for i in "${!list[@]}"; do
		# Print out list array with indeces for debugging
		#printf '${list[%s]}=%s \n' "$i" "${list[i]}"
		if [[ "${list[i]}" = \"city\" ]]; then
			local CITY="${list[i+1]} ${list[i+2]}"
		elif [[ "${list[i]}" = \"region\" ]]; then
			local REGION="${list[i+1]}"
		elif [[ "${list[i]}" = \"country\" ]]; then
			local COUNTRY="${list[i+1]}"
		fi
	done
	# Echo location information back to main function as LOCINFO for printing
	echo "Location: $CITY, $REGION, $COUNTRY"
}

# Check to see if a pipe exists on stdin.
# if pipe exists parse server data for cleaning and printing to display
if [ -p /dev/stdin ]; then
	echo "Data exists...."
	echo "Looking for lines containing the word 'connected'"
	# read the data line by line and process conditionally
	while read line; do
		for word in $line; do
			# DEBUG
			#echo "$word"
			#sleep 1.5
			if [[ $word = "connected," ]]; then
				# DEBUG: Print line with 'connected' in it and sleep 1s 
				#echo "FOUND LINE: $line"
				#sleep 1
				# Cut username out of $line
				DATE=`grep -o '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] - ' <<< "${line}"`
				TIME=`grep -o '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]' <<< "${line}"`
				USER=`cut -d \" -f 2 <<< $line | cut -d \< -f1`
				# Cut IP address out of $line
				IP=`cut -d \" -f 4 <<< $line | cut -d : -f 1`
				LOCINFO=$(locate_ip $IP)
				echo -e "$DATE$TIME > ${PURPLE}$USER${NC} connected from address ${GREEN}$IP${NC} \n \t-- ${YELLOW}${LOCINFO//\"}${NC} \n"
				sleep 1
			elif [[ $word = "disconnected" ]]; then
				DATE=`grep -o '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] - ' <<< "${line}"`
				TIME=`grep -o '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]' <<< "${line}"`
				USER=`cut -d \" -f 2 <<< $line | cut -d \< -f1`
				REASON=`grep -o '(reason \"[a-z]\"' <<< "$line"`
				echo -e "$DATE$TIME > ${PURPLE}$USER${NC} ${ORANGE}disconnected.  $REASON${NC} \n"
			elif [[ $word = "joined" ]]; then
				#case $word in
					#`grep -o '<#[a-z][a-z]>' <<< "$line"`)
					#	TEAM=`grep -o '#[a-z][a-z][a-z]' <<< "$line"`
					#	echo "CASE 1 TEAM IS: $TEAM"
					#	;;
					#`grep -o '<#[a-z][a-z][a-z]>' <<< "$line"`)
					#	TEAM=`grep -o '#[a-z][a-z]' <<< "$line"`
					#	echo "CASE 2 TEAM IS: $TEAM"
					#	;;
				#esac
				DATE=`grep -o '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] - ' <<< "${line}"`
				TIME=`grep -o '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]' <<< "${line}"`
				USER=`cut -d \" -f 2 <<< $line | cut -d \< -f1`
				TEAM=`grep -o '#[a-z][a-z]\|#[a-z][a-z][a-z]' <<< "$line"`
				echo -e "$DATE$TIME > ${PURPLE}$USER${NC} joined team ${PURPLE}${TEAM//\#}${NC} \n"
			fi 
		done
	done
else
	echo "ERROR: Pipe not found on stdin"
	if [ -f "$1" ]; then
		echo "Filename specified: ${1}"
		echo "Doing things now..................."
	else
		echo "ERROR: No input given!"
		echo "\$1 is: $1"
	fi
fi
