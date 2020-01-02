#!/usr/bin/python3

import pigpio
import signal
import time
import math

angle = 0.0
angleInc = 0.01

PWM = pigpio.pi()
if (PWM.connected()):
	print("Did you start pigpiod?")

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	PWM.hardware_PWM(12, 400, 0)
	PWM.stop()
	exit(0)

def main():
	global angle
	while True:
		PWM.hardware_PWM(12, 400, int(1000000 * pow(math.sin(2*math.pi*angle),2)))
		time.sleep(1/30)
		angle += angleInc

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()