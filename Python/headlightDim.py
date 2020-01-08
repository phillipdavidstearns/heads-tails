#!/usr/bin/python3

# import pigpio # using this for hardware PWM, software is not stable!!!
import time
import signal
import pigpio

# GPIO pin numbers

PWM_PIN = 12
PWM_FREQ = 400 # frequency of PWM
CHANNELS = 32; # number of output channels
BRIGHT=1000000
DIM=100000
FPS=30.0
PWM = pigpio.pi()
if not PWM.connected:
	exit()


def interruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	PWM.hardware_PWM(PWM_PIN, PWM_FREQ, 0)
	PWM.stop()
	exit(0)

def main():

	while True:
		theTime=int(time.time())
		print(theTime)
		if (theTime % 300 == 150):
			PWM.hardware_PWM(PWM_PIN, PWM_FREQ, BRIGHT )
		elif (theTime % 300 == 0):
			PWM.hardware_PWM(PWM_PIN, PWM_FREQ, DIM )
		time.sleep( 1/FPS )


signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

main()