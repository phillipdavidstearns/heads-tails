#!/usr/bin/python3

# csv tab of the score is publicly available at:
# https://docs.google.com/spreadsheets/d/1IF0b8Fv-7jCC3OciHavgOJIZhVEpCWoEPLl8GdaNXFA/edit#gid=1797776547
# after publishing the command to download is:
# curl -L "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1797776547&single=true&output=csv"
# (credit - https://stackoverflow.com/questions/24255472/download-export-public-google-spreadsheet-as-tsv-from-command-line)

from fileHandlers import *
import csv
import random
import time
import signal
import os
import math
import pigpio # using this for hardware PWM, software is not stable!!!
import RPi.GPIO as GPIO # using RPi.GPIO for non-PWM

#------------------------------------------------------------------------
# GPIO related
STR = 17
DATA = 27
CLK = 22
PWM_PIN = 12
PWM_FREQ = 400 # frequency of PWM
FPS = 30; # main refresh rate = frames per second

PWM = pigpio.pi()
if not PWM.connected:
	exit()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(STR, GPIO.OUT, initial=GPIO.LOW) # make pin into an output
GPIO.setup(DATA, GPIO.OUT, initial=GPIO.LOW) # make pin into an output
GPIO.setup(CLK, GPIO.OUT, initial=GPIO.LOW) # make pin into an output

def regClear():
	GPIO.output(DATA, 0)
	for i in range(CHANNELS):
		GPIO.output(CLK, 0)
		GPIO.output(CLK, 1)
	GPIO.output(CLK, 0)
	GPIO.output(STR, 1)
	GPIO.output(STR, 0)

def regOutput(channels):
	for i in range(CHANNELS):
		GPIO.output(CLK, 0)
		GPIO.output(DATA, channels[CHANNELS - i - 1])
		GPIO.output(CLK, 1)
	GPIO.output(CLK, 0)
	GPIO.output(STR, 1)
	GPIO.output(STR, 0)
	GPIO.output(DATA, 0)

#------------------------------------------------------------------------
# Behavior related

update_score=False
CHANNELS=32
channelStates=[]
eventTimes=[]
eventIndexes=[]
lastCycleTime = 0

def clearEventTimes():
	global eventTimes
	for i in range(CHANNELS):
		eventTimes.append([])

def clearChannelStates():
	global channelStates
	for i in range(CHANNELS):
		channelStates.append(0)

def clearEventIndexes():
	global eventIndexes
	for i in range(CHANNELS):
		eventIndexes.append(0)

def setLightOn(channel):
	global channelStates
	channelStates[channel] = 1

def setLightOff(channel):
	global channelStates
	channelStates[channel] = 0


def timing():

	global eventTimes
	global eventIndexes

	for c in range(CHANNELS):
		if eventTimes[c]:
			if (time.time() > eventTimes[c][0]):
				eventIndexes[c]^=1
				if (eventIndexes[c] == 1):
					setLightOn(c)
				elif (eventIndexes[c] == 0):
					setLightOff(c)
				eventTimes[c]=eventTimes[c][1:]
				if (len(eventTimes[c])==0):
					setLightOff(c)
					eventIndexes[c]^=1


def generateTimings(behavior):
	times=[]
	startTime=time.time()
	offset = random.uniform(-behavior[2],behavior[2])
	for t in range(len(behavior[0])):
		eventTime = startTime + offset + behavior[0][t] + random.uniform(-behavior[1][t],behavior[1][t])
		times.append(eventTime)
	return times

def interruptHandler(signal, frame):
	print()
	print("Interrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	regClear()
	GPIO.cleanup()
	PWM.hardware_PWM(PWM_PIN, PWM_FREQ, 0)
	PWM.stop()
	os._exit(0)

def main():

	regClear()

	clearEventTimes()
	clearChannelStates()
	clearEventIndexes()

	if update_score: updateCSV()

	behaviors = openCSV()

	global eventIndexes
	global eventTimes
	global lastCycleTime

	while True:

		cycleTime = int(time.time()) % 90 
		print("--->"+str(cycleTime)+str(channelStates),end='\r')
		if( cycleTime == 0 and cycleTime != lastCycleTime):
			startTime = time.time()
			for c in range(CHANNELS):
				index = random.randint(0,len(behaviors)-1)
				behavior = behaviors[ index ]
				eventTimes[c]+=generateTimings(behavior)
		timing()
		regOutput(channelStates)
		lastCycleTime=cycleTime
		time.sleep(1/FPS)

signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

main()