#!/usr/bin/python3/

from globalVars import *
from fileHandlers import *
from timingHandlers import *
import random
import time

def setLightOn(channel):
	global channelStates
	channelStates[channel] = 1

def setLightOff(channel):
	global channelStates
	channelStates[channel] = 0

def updateBehaviors():
	global eventTimes
	global eventIndexes
	behaviors = loadScore()
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