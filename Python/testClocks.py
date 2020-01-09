#!/usr/bin/python3

from globalVars import *
from fileHandlers import *
from gpioHandlers import *
import signal
import os
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
	os._exit(0)

def setup():
	initGPIO()
	regClear()
	resynch()

def main():
	while True:
		time.sleep(1)

signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

setup()
main()