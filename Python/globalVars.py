import time
import os
import pigpio

CHANNELS=32
FPS = 30; # refresh rate of LEDs

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