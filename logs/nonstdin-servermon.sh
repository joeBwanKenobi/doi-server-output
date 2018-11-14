#!/bin/bash
# read the data line by line and print line to console
while read line; do
	for word in $line; do
		if [ $word = "connected," ]; then
			echo "FOUND LINE: $line"
			sleep 1
			cut -d \" -f 2 <<< $line
			cut -d \" -f 4 <<< $line
			sleep 2
		fi
	done
done < testlog1.txt
