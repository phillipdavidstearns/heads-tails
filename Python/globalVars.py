import time
import os
import pigpio


CHANNELS=32
FPS = 30

INCREMENT = 1/120.0

tzOffset = -5 * 3600
dotOffset = 0 # based on the start of Phase B @ 51 seconds in the cycle starting + 28 past midnight
deviation = 0
power_line_time=time.time()

channelStates=[]
eventTimes=[]
eventIndexes=[]
lastCycleTime = 0

script_dir = os.path.split(os.path.realpath(__file__))[0]


STR = 17
DATA = 27
CLK = 22
GRID = 23

PWM_PIN = 12
PWM_FREQ = 14000 # frequency of PWM

PWM = pigpio.pi()

def init():
	global CHANNELS
	CHANNELS=32
	global FPS # refresh rate of LEDs
	FPS = 30

	global INCREMENT
	INCREMENT = 1/120.0

	global tzOffset
	tzOffset = -5 * 3600
	global dotOffset
	dotOffset = 0 # based on the start of Phase B @ 51 seconds in the cycle starting + 28 past midnight
	global deviation
	deviation = 0
	global power_line_time
	power_line_time=time.time()

	global channelStates
	channelStates=[]
	global eventTimes
	eventTimes=[]
	global eventIndexes
	eventIndexes=[]
	global lastCycleTime
	lastCycleTime = 0

	global script_dir
	script_dir = os.path.split(os.path.realpath(__file__))[0]

	# GPIO related
	global STR
	STR = 17
	global DATA
	DATA = 27
	global CLK
	CLK = 22
	global GRID
	GRID = 23

	# pigpio PWM
	global PWM_PIN
	PWM_PIN = 12
	global PWM_FREQ
	PWM_FREQ = 14000 # frequency of PWM
	# init pigpio, connect to pigpiod
	global PWM
	PWM = pigpio.pi()