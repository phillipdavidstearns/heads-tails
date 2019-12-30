#!/usr/bin/python3

import pigpio
import os
import signal
import time
import math

angle = 0.0
angleInc = 0.01

# os.system('/usr/bin/pigpiod')
PWM = pigpio.pi()

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	PWM.hardware_PWM(12, 400, 0)
	os.system('killall pigpiod')
	exit(0)

def main():
	while True:
		PWM.hardware_PWM(12, 400, int( 1000000 * pow( math.sin( 2*math.pi*angle),2)))
		time.sleep(1/30)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()