#!/usr/bin/python3

import pigpio
import signal
import time
import math

angle = 0.0
angleInc = 0.01

try:
	PWM = pigpio.pi()
except:
	print("Is pigpiod running?")
	exit()
	
def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	PWM.hardware_PWM(12, 400, 0)
	PWM.stop()
	exit(0)

def main():
	global angle
	while True:
		try:
			PWM.hardware_PWM(12, 400, int(1000000 * pow(math.sin(2*math.pi*angle),2)))
		except:
			print("Is pigpiod running?")
			exit()
		time.sleep(1/30)
		angle += angleInc

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()