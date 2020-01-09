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

def resynch():
	global power_line_time
	global deviation
	fetchDeviation()
	deviation = loadDeviation()
	power_line_time=time.time()


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

	headlights = loadHeadlights()


def main():

	global eventTimes
	global eventIndexes
	global channelStates
	global lastCycleTime
	global power_line_time

	headlights = loadHeadlights()

	while True:

		print(" LocalTime: "+str(time.time())+", AdjustedTime: "+str(adjustedTime(),end='\'')
		time.sleep(.1)


signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

setup()
main()