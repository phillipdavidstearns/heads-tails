#!/usr/bin/python3


import time # for basic timing modules like sleep() and time()
import signal
import subprocess
import datetime

DEBUG = True

tzOffset = -5 * 3600
dotOffset = 17 # based on the start of Phase B @ 51 seconds in the cycle starting + 28 past midnight
drift = 0

DOTTime = 0
tc = time.time()
tp = 0.0
dt = 1.0
cycle = 90.0

def updateRegisters(data=0):
	pass
	# print("{0:b}".format(int(data)))
	# print("{0:b}".format(int(data) >> 1 & 1))

def dotSeconds():
	# resource on synching raspberry pi https://raspberrytips.com/time-sync-raspberry-pi/
	# the python3.7 time module https://docs.python.org/3.7/library/time.html

	# capture timestamp from DOT server
	cmd="curl http://207.251.86.238/ -I 2>/dev/null | grep Date | grep -oE '([0-9]{2}:){2}[0-9]{2}'"

	try:
		time,error = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
	except:
		print("Unable to contact server.")
		return 0

	time_dot = str(time,'utf-8').strip().split(':')
	#convert timestamp to local seconds
	dot_seconds = int(time_dot[0])*3600 + int(time_dot[1])*60 + int(time_dot[2]) # raw GMT server time
	dot_seconds += tzOffset # offsets based on timezone adjustments
	dot_seconds = (dot_seconds + 86400) % 86400 # wrap around midnight

	return dot_seconds

def localSeconds():
	# capture localtime
	time_local = time.localtime()
	# convert to seconds
	local_seconds = int(time_local[3])*3600 + int(time_local[4])*60 + int(time_local[5])
	return local_seconds

def timeDrift():
	return dotSeconds() - localSeconds()

def runTheCode():
	if DEBUG:
		displaySynch()

def displaySynch():
	cycle = (localSeconds() + dotOffset + drift) % 90
	print(cycle)
	if(cycle == 0):
		print("Green")
	if(cycle == 34):
		print("Amber")
	if(cycle == 36):
		print("Red")


def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	# exit(0)

def main():

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
			runTheCode()

		time.sleep(0.1)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()