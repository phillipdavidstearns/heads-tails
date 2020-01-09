import pigpio # using this for hardware PWM, software is not stable!!!
import RPi.GPIO as GPIO # using RPi.GPIO for non-PWM

#------------------------------------------------------------------------
# GPIO related
STR = 17
DATA = 27
CLK = 22
GRID = 23
# pigpio PWM
PWM_PIN = 12
PWM_FREQ = 14000 # frequency of PWM
# init pigpio, connect to pigpiod
PWM = pigpio.pi()
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