from globalVars import *
import pigpio # using this for hardware PWM, software is not stable!!!
import RPi.GPIO as GPIO # using RPi.GPIO for non-PWM
import subprocess
import time

def incrementCounter(channel):
	global power_line_time
	power_line_time += INCREMENT
	print("power_line_time: "+str(power_line_time),end='\r')

#------------------------------------------------------------------------

if not PWM.connected:
	exit()

#------------------------------------------------------------------------
# RPi.GPIO

def initGPIO():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(STR, GPIO.OUT, initial=GPIO.LOW) # make pin into an output
	GPIO.setup(DATA, GPIO.OUT, initial=GPIO.LOW) # make pin into an output
	GPIO.setup(CLK, GPIO.OUT, initial=GPIO.LOW) # make pin into an output
	GPIO.setup(GRID, GPIO.IN) # make pin into an input
	GPIO.add_event_detect(GRID, GPIO.BOTH, callback=incrementCounter)

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