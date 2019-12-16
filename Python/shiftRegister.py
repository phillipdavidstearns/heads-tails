#!/usr/bin/python3

import time
import signal
import RPi.GPIO as GPIO # using RPi.GPIO
import random

STR = 17
DATA = 27
CLK = 22
CHANNELS = 32; # number of output channels
FPS = 30; # refresh rate = frames per second
counter = 0

def pinSetup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(STR, GPIO.OUT) # make pin into an output
	GPIO.setup(DATA, GPIO.OUT) # make pin into an output
	GPIO.setup(CLK, GPIO.OUT) # make pin into an output

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
		GPIO.output(DATA, value >> ((CHANNELS - i - 1) % 8)  & 1)
		GPIO.output(CLK, 1)
	GPIO.output(CLK, 0)
	GPIO.output(STR, 1)
	GPIO.output(STR, 0)
	GPIO.output(DATA, 0)

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	regClear()
	# custom GPIO cleanup
	GPIO.setup(STR, GPIO.IN)
	GPIO.setup(DATA, GPIO.IN)
	GPIO.setup(CLK, GPIO.IN)
	exit(0)

def main():

	print("Raspi GPIO ShiftRegister Test")
	print("Ctrl C to quit")

	global counter

	pinSetup()
	regClear()

	while True:
		regOutput(counter)
		counter += 1
		time.sleep(1/FPS)

signal.signal(signal.SIGINT, keyboardInterruptHandler)
main()
