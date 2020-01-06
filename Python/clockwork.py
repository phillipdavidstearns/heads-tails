#!/usr/bin/python3/

# csv tab of the score is publicly available at:
# https://docs.google.com/spreadsheets/d/1IF0b8Fv-7jCC3OciHavgOJIZhVEpCWoEPLl8GdaNXFA/edit#gid=1797776547
# after publishing the command to download is:
# curl -L "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1797776547&single=true&output=csv"
# (credit - https://stackoverflow.com/questions/24255472/download-export-public-google-spreadsheet-as-tsv-from-command-line)

import csv
import random
import time
import random
import signal
import os
import subprocess

CHANNELS=32

headlightTimes=[ 26400, 60300 ] # default sunrise/sunset times
headlightState=0 # 0 for dim 1 for bright
lastHeadlightState=0 # 0 for dim 1 for bright

tzOffset = -5 * 3600
dotOffset = 14 # based on the start of Phase B @ 51 seconds in the cycle starting + 28 past midnight
drift = 0
deviation = 0

DOTTime = 0
tc = time.time()
tp = 0.0
dt = 1.0
cycle = 90.0

script_dir = os.path.split(os.path.realpath(__file__))[0]

def updateHeadlightsCSV():
	cmd = 'curl --connect-timeout 5 -m 10 -L '
	cmd += '"https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1716879590&single=true&output=csv"'
	temp_filename = '"' + script_dir + '/data/headlights_temp.csv' +  '"'
	filename = '"' + script_dir + '/data/headlights.csv' +  '"'
	cmd +=' > ' + temp_filename
	update = -1

	try:
		update = os.system(cmd)
	except:
		print("Couldn't update headlight timings")

	if ( update == 0 ):
		os.system("mv "+temp_filename+" "+filename)
	else:
		print("curl completed with a non-zero exit status")
		os.system("rm "+temp_filename)

def updateDeviation():
	global deviation
	cmd = 'curl --connect-timeout 5 -m 10 -L '
	cmd += '"https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=913901720&single=true&output=csv"'
	temp_filename = '"' + script_dir + '/data/deviation_temp.txt' +  '"'
	filename = '"' + script_dir + '/data/deviation.txt' +  '"'
	cmd +=' > ' + temp_filename
	update = -1

	try:
		update = os.system(cmd)
	except:
		print("Couldn't update deviation")

	if ( update == 0 ):
		os.system("mv "+temp_filename+" "+filename)
	else:
		print("curl completed with a non-zero exit status")
		os.system("rm "+temp_filename)

	return loadDeviation()
	
# A demo of readlines()
 
def loadDeviation():
	with open( script_dir + "/data/deviation.txt",'rt') as f:
		deviation = f.read()
	return int(deviation)

def loadHeadlightTimes():
	with open( script_dir + "/data/headlights.csv",'rt') as f:
		reader = csv.reader(f)
		headlights= {}
		for row in reader:
			date=row[0]
			onTime=row[1]
			offTime=row[2]
			headlights[date]=[onTime,offTime]

	return headlights

def dotSeconds():
	# resource on synching raspberry pi https://raspberrytips.com/time-sync-raspberry-pi/
	# the python3.7 time module https://docs.python.org/3.7/library/time.html

	# capture timestamp from DOT server
	cmd='curl http://207.251.86.238/ -I 2>/dev/null | grep Date | grep -oE \'([0-9]{2}:){2}[0-9]{2}\''

	try:
		time,error = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
	except:
		print("Unable to contact server.")
		return 0

	dotTime = str(time,'utf-8').strip().split(':')
	#convert timestamp to local seconds
	dotSeconds = int(dotTime[0])*3600 + int(dotTime[1])*60 + int(dotTime[2]) # raw GMT server time
	dotSeconds += tzOffset # offsets based on timezone adjustments
	dotSeconds = (dotSeconds + 86400) % 86400 # wrap around midnight

	return dotSeconds

def localSeconds():
	# capture localtime
	localTime = time.localtime()
	# convert to seconds
	localSeconds = int(localTime[3])*3600 + int(localTime[4])*60 + int(localTime[5])
	return localSeconds

def timeDrift():
	return dotSeconds() - localSeconds()

def adjustedTime():
	return localSeconds() + dotOffset + drift + deviation

def displaySynch(time):
	cycle = time  % 90
	# print(cycle)
	if(cycle == 0):
		print("Green")
	if(cycle == 34):
		print("Amber")
	if(cycle == 37):
		print("Red")

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	os._exit(0)

def main():
	updateDeviation()

	#-----headlight stuff
	headlights=loadHeadlightTimes()
	date=str(time.localtime()[1])+'/'+str(time.localtime()[2])

	try:
		global headlightTimes
		dim = headlights[date][0].split(':')
		bright = headlights[date][1].split(':')
		headlightTimes[0]=int(dim[0])*3600+int(dim[1])*60
		headlightTimes[1]=int(bright[0])*3600+int(bright[1])*60
	except:
		pass
	
	#-----clock stuff
	global tc
	global tp
	global drift

	try:
		drift = timeDrift()
	except:
		print("Unable to get DOT server timestamp.")
		drift = 0

	print("Local clock is off by: " + str(drift))

	while True:
		tc = time.time()
		if (tc - tp >= dt):
			tp = tc
			displaySynch(adjustedTime())

		time.sleep(0.01)



signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()