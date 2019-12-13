#!/usr/bin/python3

import csv # read csv files
from time import * # for basic timing modules like sleep() and time()
# import RPi.GPIO as GPIO
from threading import Timer
import subprocess

DOTTime = 0
tc = time()
tp = 0.0
dt = 1.0
cycle = 90.0

# def reference(): # Just keeping this here to remind me of how things work ;)
# 	# to use Raspberry Pi board pin numbers
# 	GPIO.setmode(GPIO.BOARD)
	 
# 	# set up the GPIO channels - one input and one output
# 	GPIO.setup(11, GPIO.IN)
# 	GPIO.setup(12, GPIO.OUT)
	 
# 	# input from pin 11
# 	input_value = GPIO.input(11)
	 
# 	# output to pin 12
# 	GPIO.output(12, GPIO.HIGH)
	 
# 	# the same script as above but using BCM GPIO 00..nn numbers
# 	GPIO.setmode(GPIO.BCM)
# 	GPIO.setup(17, GPIO.IN)
# 	GPIO.setup(18, GPIO.OUT)
# 	input_value = GPIO.input(17)
# 	GPIO.output(18, GPIO.HIGH)

def updateRegisters(data=0):
	print("{0:b}".format(int(data)))
	print("{0:b}".format(int(data) >> 1 & 1))

def getDOTTime():
	# resource on synching raspberry pi https://raspberrytips.com/time-sync-raspberry-pi/
	global DOTTime
	cmd="curl http://207.251.86.238/ -I 2>/dev/null | grep Date | grep -oE '([0-9]{2}:){2}[0-9]{2}'"
	DOTTime,error = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def runTheCode():
	theTime = time()
	print("Global Time?: " + str(theTime))
	print("theTime % " + str(cycle) + " : " + str(theTime % cycle))
	updateRegisters(theTime)


def main():

	global tc
	global tp

	tc = time()
	if (tc - tp >= dt):
		tp = tc
		runTheCode()

	sleep(0.01)

t = Timer(5.0, runTheCode)
t.start()

sleep(6)
exit()

# while True:
# 	main()
