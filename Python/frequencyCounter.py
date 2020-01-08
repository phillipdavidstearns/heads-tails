#!/usr/bin/python3

# import pigpio # using this for hardware PWM, software is not stable!!!
import signal
import time
import RPi.GPIO as GPIO # using RPi.GPIO for non-PWM

power_line_time=0.0
start_time=0.0
# GPIO pin numbers
INPUT = 23
FPS = 30; # main refresh rate = frames per second
INCREMENT = 1/120.0

def incrementCounter(channel):
	global power_line_time
	power_line_time += INCREMENT

def interruptHandler(signal, frame):
	print()
	print("Interrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	exit(0)

def init():
	global start_time
	global power_line_time
	start_time=time.time()
	power_line_time=time.time()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT, GPIO.IN) # make pin into an input
	GPIO.add_event_detect(INPUT, GPIO.BOTH, callback=incrementCounter)

def main():
	while True:
		realTime=time.time()
		print("   LocalTime: "+str(realTime)+", PowerLineTime: "+str(power_line_time)+", Deviation: "+str(realTime-power_line_time), end='\r')
		time.sleep( 1 / FPS )

signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

init()
main()