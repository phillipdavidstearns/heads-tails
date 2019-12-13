#!/usr/bin/python3

import time
import signal
import RPi.GPIO as GPIO # using RPi.GPIO
import random

STR = 17
DATA = 27
CLK = 22
PULSE = 0.0

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

def main():
	while True:
		regOutput()
		time.sleep(1/30.0)

def regOutput():
	for i in range(8):
		GPIO.output(CLK,0)
		time.sleep(PULSE)
		GPIO.output(DATA, random.randint(0,1))
		time.sleep(PULSE)
		GPIO.output(CLK,1)
		time.sleep(PULSE)
	GPIO.output(CLK,0)
	time.sleep(PULSE)
	GPIO.output(STR,1)
	time.sleep(PULSE)
	GPIO.output(STR,0)
	time.sleep(PULSE)
	GPIO.output(DATA,0)

main()
