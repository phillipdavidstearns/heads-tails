#!/usr/bin/python3

import time
import signal
import RPi.GPIO as GPIO # using RPi.GPIO
import random
import math

# GPIO pin numbers
STR = 17
DATA = 27
CLK = 22
PWM = 12

FREQUENCY = 400 # frequency of PWM
CHANNELS = 32; # number of output channels
FPS = 30; # main refresh rate = frames per second
counter = 0
angle = 0.0
angleInc = 0.001
value = 0b11111111111111111111111111111111 # testing purposes

GPIO.setmode(GPIO.BCM)
GPIO.setup(STR, GPIO.OUT, initial=GPIO.LOW) # make pin into an output
GPIO.setup(DATA, GPIO.OUT, initial=GPIO.LOW) # make pin into an output
GPIO.setup(CLK, GPIO.OUT, initial=GPIO.LOW) # make pin into an output
GPIO.setup(PWM, GPIO.OUT)
headLights = GPIO.PWM(PWM, FREQUENCY)
headLights.start(0)

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

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	regClear()
	GPIO.cleanup()
	exit(0)

def main():

	print("Raspi GPIO ShiftRegister Test")
	print("Ctrl C to quit")

	global counter
	global value
	global angle

	regClear()

	while True:
#		value = 1 << ( counter % CHANNELS )
		for i in range( CHANNELS ):
			if ( counter % ( i + 10 ) == 0 ):
				value ^= 1 << i
		regOutput( value )
		if (counter % 300 == 150):
			headLights.ChangeDutyCycle( 100.0 )
		elif (counter % 300 == 0):
			headLights.ChangeDutyCycle( 10.0 )
		angle += angleInc
		counter += 1
		time.sleep( 1 / FPS )

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()
