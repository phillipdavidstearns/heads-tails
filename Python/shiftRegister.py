#!/usr/bin/python3

import time
import signal
import RPi.GPIO as GPIO # using RPi.GPIO

STR = 17
DATA = 27
CLK = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(STR, GPIO.OUT) # make pin into an output
GPIO.setup(DATA, GPIO.OUT) # make pin into an output
GPIO.setup(CLK, GPIO.OUT) # make pin into an output

print("Raspi GPIO Hello World")
print("Ctrl C to quit")

def keyboardInterruptHandler(signal, frame):
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	GPIO.cleanup()
	exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

while True:
	GPIO.output(4,0)
	time.sleep(0.30)
	GPIO.output(4,1)
	time.sleep(0.30)

def regOutput():
	GPIO.output(CLK,