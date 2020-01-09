#!/usr/bin/python3

from fileHandlers import *
import signal
import os
import pigpio # using this for hardware PWM, software is not stable!!!
import RPi.GPIO as GPIO # using RPi.GPIO for non-PWM
import random
import time

#------------------------------------------------------------------------

CHANNELS=32
FPS = 30

INCREMENT = 1/120.0

tzOffset = -5 * 3600
dotOffset = -26 # based on the start of Phase B @ 51 seconds in the cycle starting + 28 past midnight
deviation = 0
power_line_time=time.time()

behaviors=[]
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

DIM = 0.15
BRIGHT = 1.0

PWM = pigpio.pi()

if not PWM.connected:
	exit()

def adjustedTime():
	return power_line_time + tzOffset + dotOffset + deviation

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

def incrementCounter(channel):
	global power_line_time
	power_line_time += INCREMENT

#------------------------------------------------------------------------

headlightTimes=[ 26400, 60300 ] # default sunrise/sunset times
headlightState=0 # 0 for dim 1 for bright
lastHeadlightState=0 # 0 for dim 1 for bright

def updateHeadlightTimes():
	date=str(time.localtime()[1])+'/'+str(time.localtime()[2])
	
	try: # if the date is accounted for, we good
		global headlightTimes
		dim = headlights[date][0].split(':')
		bright = headlights[date][1].split(':')
		headlightTimes[0]=int(dim[0])*3600+int(dim[1])*60
		headlightTimes[1]=int(bright[0])*3600+int(bright[1])*60
	except: # otherwise we go with the defaults or last used
		pass

def updateHeadlights():
	headlightTime=int(adjustedTime())%86400
	if ( headlightTime >= headlightTimes[0] and  headlightTime < headlightTimes[1] ):
		PWM.hardware_PWM(PWM_PIN, PWM_FREQ, int(DIM*1000000) ) # dim
	else:
		PWM.hardware_PWM(PWM_PIN, PWM_FREQ, int(BRIGHT*1000000) ) # bright

def resynch():
	global power_line_time
	global deviation
	fetchDeviation()
	deviation = loadDeviation()
	power_line_time=time.time()

#------------------------------------------------------------------------

def setLightOn(channel):
	global channelStates
	channelStates[channel] = 1

def setLightOff(channel):
	global channelStates
	channelStates[channel] = 0

def updateBehaviors():
	global eventTimes
	global eventIndexes
	global behaviors
	behaviorList=makeBehaviorList(behaviors)
	for c in range(CHANNELS):
		behavior = behaviors[behaviorList[c]]
		timings=generateTimings(behavior)
		eventTimes[c]+=timings[0]
		eventIndexes[c]+=timings[1]

def updateOutput():
	global eventTimes
	global eventIndexes
	for c in range(CHANNELS):
		if eventTimes[c]:
			if (adjustedTime() > eventTimes[c][0]):
				if (eventIndexes[c][0] == 1):
					setLightOn(c)
				elif (eventIndexes[c][0] == 0):
					setLightOff(c)
				# remove the event from queue
				eventIndexes[c]=eventIndexes[c][1:]
				eventTimes[c]=eventTimes[c][1:]
				if (len(eventTimes[c])==0):
					setLightOff(c)

def generateTimings(behavior):
	times=[]
	indexes=[]
	offset = random.uniform(-behavior[2],behavior[2])
	startTime=adjustedTime()
	for t in range(len(behavior[0])):
		eventTime = startTime + offset + behavior[0][t] + random.uniform(-behavior[1][t],behavior[1][t])
		times.append(eventTime)
		if (t%2==0):
			indexes.append(1)
		else:
			indexes.append(0)
	return [times, indexes]

def makeBehaviorList(behaviors):
	behaviorList=[]
	itemCount=[0]*len(behaviors)
	while (len(behaviorList) < CHANNELS):
		candidate=random.randint(0,len(behaviors)-1)
		if (itemCount[candidate] < 2):
			itemCount[candidate] += 1
			behaviorList.append(random.randint(0,len(behaviors)-1))
	return behaviorList

#------------------------------------------------------------------------

def interruptHandler(signal, frame):
	print()
	print("Interrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	regClear()
	GPIO.cleanup()
	PWM.hardware_PWM(PWM_PIN, PWM_FREQ, 0)
	PWM.stop()
	os._exit(0)

def setup():
	global eventTimes
	global eventIndexes
	global channelStates
	global behaviors

	for i in range(CHANNELS):
		eventTimes.append([])
		eventIndexes.append([])
		channelStates.append(0)

	initGPIO()
	regClear()
	fetchScore()
	resynch()
	updateHeadlightTimes()
	headlights = loadHeadlights()
	behaviors = loadScore()

def main():

	global eventTimes
	global eventIndexes
	global channelStates
	global lastCycleTime
	global power_line_time

	while True:

		updateHeadlights()

		cycleTime = int(adjustedTime()) % 90
		localTime = time.localtime()
		print(" cycle: "+str(cycleTime)
			+", plt: "+str(int(power_line_time))
			+", adj: "+str(int(adjustedTime()))
			+", local: "+str(int(time.time()))
			+f" - H: {localTime[3]:02d}"
			+f" M: {localTime[4]:02d}"
			+f" S: {localTime[5]:02d}"
			,end='\r')
		if( cycleTime == 0 and cycleTime != lastCycleTime):
			updateBehaviors()

		updateOutput()

		regOutput(channelStates)

		lastCycleTime=cycleTime
		time.sleep(1/FPS)

signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

setup()
main()