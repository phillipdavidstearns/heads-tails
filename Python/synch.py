#!/usr/bin/python3

import csv # read csv files
from time import * # for basic timing modules like sleep() and time()
# import RPi.GPIO as GPIO
import signal
from threading import Timer
import subprocess
import datetime

DOTTime = 0
tc = time()
tp = 0.0
dt = 1.0
cycle = 90.0

def updateRegisters(data=0):
	print("{0:b}".format(int(data)))
	print("{0:b}".format(int(data) >> 1 & 1))

def getDOTTime():
	# resource on synching raspberry pi https://raspberrytips.com/time-sync-raspberry-pi/
	cmd="curl http://207.251.86.238/ -I 2>/dev/null | grep Date | grep -oE '([0-9]{2}:){2}[0-9]{2}'"
	time,error = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
	print(str(time,'utf-8').strip().split(':'))
	return time

def runTheCode():
	theTime = time()
	print("DOTTime: " + str(getDOTTime(), 'utf-8').strip())
	print("Global Time: " + str(theTime))
	print("theTime % " + str(cycle) + " : " + str(theTime % cycle))
	print( str(datetime.timedelta(seconds = theTime)) )
	print(strftime("%H:%M:%S", gmtime(theTime)))
	updateRegisters(theTime)


def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	#regClear()
	#GPIO.cleanup()
	exit(0)

def main():

	global tc
	global tp
	while True:
		tc = time()
		if (tc - tp >= dt):
			tp = tc
			runTheCode()

		sleep(0.01)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()