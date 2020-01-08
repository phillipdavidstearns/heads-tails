#!/usr/bin/python3

# import pigpio # using this for hardware PWM, software is not stable!!!
import signal
import time
import RPi.GPIO as GPIO # using RPi.GPIO for non-PWM

init=True
power_line_time=0.0
start_time=0.0
# GPIO pin numbers
INPUT = 23
FPS = 30; # main refresh rate = frames per second
INCREMENT = 1/120.0

def incrementCounter():
	power_line_time += INCREMENT

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT, GPIO.IN) # make pin into an input
GPIO.add_event_detect(INPUT, GPIO.BOTH, incrementCounter)

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	regClear()
	GPIO.cleanup()
	exit(0)

def main():
	global start_time
	global power_line_time
	global init
	if init:
		start_time=time.time()
		power_line_time=time.time()
		init=False
	while True:
		print("   LocalTime: "+str(time.time())+", PowerLineTime: "+str(power_line_time), end='\r')
		time.sleep( 1 / FPS )

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()