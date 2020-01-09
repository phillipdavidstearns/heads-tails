#!/usr/bin/python3

from globalVars import *
from fileHandlers import *
from timingHandlers import *
import signal
import os

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
	os._exit(0)

def setup():
	initGPIO()
	regClear()

def main():
	while True:
		print(" dev: "+str(deviation)
			+", PLT: "+str(power_line_time)
			+", LocalTime: "+str(time.time())
			+", AdjustedTime: "+str(adjustedTime()),
			end='\r')
		time.sleep(.1)

signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

setup()
main()