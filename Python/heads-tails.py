#!/usr/bin/python3

from fileHandlers import *
import random
import time
import signal
import os
import math
import pigpio # using this for hardware PWM, software is not stable!!!
import RPi.GPIO as GPIO # using RPi.GPIO for non-PWM

#------------------------------------------------------------------------

CHANNELS=32
FPS = 30; # refresh rate of LEDs

#------------------------------------------------------------------------

headlightTimes=[ 26400, 60300 ] # default sunrise/sunset times
headlightState=0 # 0 for dim 1 for bright
lastHeadlightState=0 # 0 for dim 1 for bright

#------------------------------------------------------------------------

tzOffset = -5 * 3600
dotOffset = 12 # based on the start of Phase B @ 51 seconds in the cycle starting + 28 past midnight
drift = 0 # calculated based on onboard frequency counting
deviation = 0

# grid synch related
start_time=time.time()
power_line_time=start_time
INCREMENT = 1/120.0

def incrementCounter(channel):
	global power_line_time
	power_line_time += INCREMENT
	
def dotSeconds():
	# resource on synching raspberry pi https://raspberrytips.com/time-sync-raspberry-pi/
	# the python3.7 time module https://docs.python.org/3.7/library/time.html

	# capture timestamp from DOT server
	cmd='curl http://207.251.86.238/ -I 2>/dev/null | grep Date | grep -oE \'([0-9]{2}:){2}[0-9]{2}\''

	try:
		time,error = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
	except:
		print("Unable to contact server.")
		return 0

	dotTime = str(time,'utf-8').strip().split(':')

	dotSeconds = int(dotTime[0])*3600 + int(dotTime[1])*60 + int(dotTime[2]) #convert timestamp to local seconds
	dotSeconds += tzOffset # offsets based on timezone adjustments
	dotSeconds += 86400 # wrap around midnight
	dotSeconds %= 86400 # wrap around midnight

	return dotSeconds

def localSeconds():
	localTime = time.localtime() # capture localtime
	localSeconds = int(localTime[3])*3600 + int(localTime[4])*60 + int(localTime[5]) # convert to seconds
	return localSeconds

def timeDrift():
	return dotSeconds() - localSeconds()

def adjustedTime():
	return int(power_line_time + dotOffset + deviation + tzOffset)

#------------------------------------------------------------------------
# GPIO related
STR = 17
DATA = 27
CLK = 22
GRID = 23
# pigpio PWM
PWM_PIN = 12
PWM_FREQ = 400 # frequency of PWM
PWM = pigpio.pi()
if not PWM.connected:
	exit()

#------------------------------------------------------------------------
# RPi.GPIO

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

#------------------------------------------------------------------------
# Behavior related

CHANNELS=32

channelStates=[]
eventTimes=[]
eventIndexes=[]
lastCycleTime = 0


def setLightOn(channel):
	global channelStates
	channelStates[channel] = 1

def setLightOff(channel):
	global channelStates
	channelStates[channel] = 0

def timing():

	global eventTimes
	global eventIndexes

	for c in range(CHANNELS):
		if eventTimes[c]:
			if (time.time() > eventTimes[c][0]):
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
	startTime=time.time()
	offset = random.uniform(-behavior[2],behavior[2])
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

def interruptHandler(signal, frame):
	print()
	print("Interrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	regClear()
	GPIO.cleanup()
	PWM.hardware_PWM(PWM_PIN, PWM_FREQ, 0)
	PWM.stop()
	os._exit(0)

def main():

	global eventTimes
	global eventIndexes
	global channelStates
	global lastCycleTime

	for i in range(CHANNELS):
		eventTimes.append([])
		eventIndexes.append([])
		channelStates.append(0)

	regClear()
	behaviors = loadScore()
	behaviorList=makeBehaviorList(behaviors)

	#-----synch

	updateDeviation()

	#-----headlight stuff
	headlights=loadHeadlights()
	date=str(time.localtime()[1])+'/'+str(time.localtime()[2])
	
	try: # if the date is accounted for, we good
		global headlightTimes
		dim = headlights[date][0].split(':')
		bright = headlights[date][1].split(':')
		headlightTimes[0]=int(dim[0])*3600+int(dim[1])*60
		headlightTimes[1]=int(bright[0])*3600+int(bright[1])*60
	except: # otherwise we go with the defaults or last used
		pass

	while True:

		headlightTime=adjustedTime()
		if ( headlightTime >= headlightTimes[0] and  headlightTime < headlightTimes[1] ):
			PWM.hardware_PWM(PWM_PIN, PWM_FREQ, 100000 ) # dim
		else:
			PWM.hardware_PWM(PWM_PIN, PWM_FREQ, 1000000 ) # bright

		cycleTime = adjustedTime() % 90

		# realTime=time.time()
		# print("   LocalTime: "+str(realTime)+", PowerLineTime: "+str(power_line_time)+", Deviation: "+str(realTime-power_line_time), end='\r')
		
		# print("--->"+str(headlightTimes)+" "+str(tempTime)+" "+str(headlightTime)+" {:02d} ".format(cycleTime)+str(channelStates),end='\r')
		
		if( cycleTime == 0 and cycleTime != lastCycleTime):
			for c in range(CHANNELS):
				behavior = behaviors[behaviorList[c]]
				timings=generateTimings(behavior)
				eventTimes[c]+=timings[0]
				eventIndexes[c]+=timings[1]
		timing()
		regOutput(channelStates)
		lastCycleTime=cycleTime
		time.sleep(1/FPS)

signal.signal(signal.SIGINT, interruptHandler)
signal.signal(signal.SIGTERM, interruptHandler)

main()