#!/usr/bin/python3

# csv tab of the score is publicly available at:
# https://docs.google.com/spreadsheets/d/1IF0b8Fv-7jCC3OciHavgOJIZhVEpCWoEPLl8GdaNXFA/edit#gid=1797776547
# after publishing the command to download is:
# curl -L "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1797776547&single=true&output=csv"
# (credit - https://stackoverflow.com/questions/24255472/download-export-public-google-spreadsheet-as-tsv-from-command-line)

import csv
from threading import Timer
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

def regOutput(value):
	for i in range(CHANNELS):
		GPIO.output(CLK, 0)
		GPIO.output(DATA, value >> (CHANNELS - i - 1)  & 1)
		GPIO.output(CLK, 1)
	GPIO.output(CLK, 0)
	GPIO.output(STR, 1)
	GPIO.output(STR, 0)
	GPIO.output(DATA, 0)

#------------------------------------------------------------------------
# Behavior related

update_score=False
last_cycle=0
CHANNELS=32
channelStates=[]

for i in range(CHANNELS):
	channelStates.append(0)

curl = 'curl --connect-timeout 5 -m 10 -L "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1797776547&single=true&output=csv"'
temp_filename = "\"" + os.path.dirname(__file__) + "/data/score_temp.csv" +  "\""
filename = "\"" + os.path.dirname(__file__) + "/data/score.csv" +  "\""
cmd = curl+" > "+temp_filename


def setLightOn(channel):
	global channelStates
	channelStates[channel] = 1


def setLightOff(channel):
	global channelStates
	channelStates[channel] = 0

def updateCSV():
	update = -1
	try:
		update = os.system(cmd)
		print(update)
	except:
		print("Couldn't update sheet")

	if ( update == 0 ):
		os.system("mv "+temp_filename+" "+filename)
	else:
		os.system("rm "+temp_filename)
		print("curl completed with a non-zero exit status")

def openCSV():
	with open( os.path.dirname(__file__) + "/data/score.csv",'rt') as f:
		reader = csv.reader(f)
		behaviors=[]
		for row in reader:
			index=0
			times=[]
			variations=[]
			offset_variation=0
			for item in row:
				temp = -1.0

				if item: # execute if string isn't empty
					try: # convert appropriate strings to float
						temp=float(item)
					except:
						pass

					if (temp != -1): # test if a conversion happened
						if (index == 0):
							offset_variation=(temp)
						elif (index % 2 == 1):
							times.append(temp)
						else:
							variations.append(temp)
						index += 1
			behaviors.append(list([times,variations,offset_variation]))
	return behaviors


def printBehavior(behavior):
	for i, timing in enumerate(behavior):
		print(behavior[i])

def createTimers(behavior, whichChannel=0):
	timers=[]
	offset = random.uniform(-behavior[2],behavior[2])
	for i in range(len(behavior[0])):
		delay = offset + behavior[0][i] + random.uniform(-behavior[1][i],behavior[1][i])
		if (i % 2 == 0):
			timers.append(Timer(delay,setLightOn,[whichChannel]))
		else:
			timers.append(Timer(delay,setLightOff,[whichChannel]))
	return timers

def initiateTimers(timers):
	for t in timers:
		t.start()

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	regClear()
	GPIO.cleanup()
	PWM.hardware_PWM(PWM_PIN, PWM_FREQ, 0)
	PWM.stop()
	os._exit(0)

def main():
	regClear()
	if update_score: updateCSV()

	behaviors = openCSV()

	while True:
		cycleTime = int(time.time()) % 90 
		print("----| " + str(cycleTime)+str(channelStates),end='\r')
		
		if( cycleTime == 0 && cycleTime != last_cycle ):
			for i in range(CHANNELS):
				index = random.randint(0,len(behaviors)-1)
				behavior = behaviors[ index ]
				initiateTimers(createTimers(behavior, i))
		last_cycle = cycleTime
		time.sleep(1/FPS)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()