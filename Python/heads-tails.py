#!/usr/bin/python3

from globalVars import *
from fileHandlers import *
from timingHandlers import *
from behaviorHandlers import *
from gpioHandlers import *
import signal
import os
import pigpio # using this for hardware PWM, software is not stable!!!
import RPi.GPIO as GPIO # using RPi.GPIO for non-PWM

#------------------------------------------------------------------------

headlightTimes=[ 26400, 60300 ] # default sunrise/sunset times
headlightState=0 # 0 for dim 1 for bright
lastHeadlightState=0 # 0 for dim 1 for bright

def resynch():
	global power_line_time
	global deviation
	fetchDeviation()
	deviation = loadDeviation()
	power_line_time=time.time()

def updateHeadlightTimes():
	date=str(time.localtime()[1])+'/'+str(time.localtime()[2])
	
	try: # if the date is accounted for, we good
		global headlightTimes
		dim = headlights[date][0].split(':')
		bright = headlights[date][1].split(':')
		headlightTimes[0]=int(dim[0])*3600+int(dim[1])*60
		headlightTimes[1]=int(bright[0])*3600+int(bright[1])*60
	except: # otherwise we go with the defaults or last used
		pass

def updateHeadlights():
	headlightTime=adjustedTime()
	if ( headlightTime >= headlightTimes[0] and  headlightTime < headlightTimes[1] ):
		PWM.hardware_PWM(PWM_PIN, PWM_FREQ, DIM ) # dim
	else:
		PWM.hardware_PWM(PWM_PIN, PWM_FREQ, BRIGHT ) # bright

def interruptHandler(signal, frame):
	print()
	print("Interrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	regClear()
	GPIO.cleanup()
	PWM.hardware_PWM(PWM_PIN, PWM_FREQ, 0)
	PWM.stop()
	os._exit(0)

def setup():
	global eventTimes
	global eventIndexes
	global channelStates

	for i in range(CHANNELS):
		eventTimes.append([])
		eventIndexes.append([])
		channelStates.append(0)

	initGPIO()
	regClear()
	fetchScore()
	resynch()

def main():

	global eventTimes
	global eventIndexes
	global channelStates
	global lastCycleTime
	global power_line_time

	headlights = loadHeadlights()

	while True:

		cycleTime = adjustedTime() % 90

		if( cycleTime == 0 and cycleTime != lastCycleTime):
			updateBehaviors()
		updateOutput()
		regOutput(channelStates)
		lastCycleTime=cycleTime
		time.sleep(1/FPS)

signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

setup()
main()