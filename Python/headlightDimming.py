#!/usr/bin/python3/

# csv tab of the score is publicly available at:
# https://docs.google.com/spreadsheets/d/1IF0b8Fv-7jCC3OciHavgOJIZhVEpCWoEPLl8GdaNXFA/edit#gid=1797776547
# after publishing the command to download is:
# curl -L "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1797776547&single=true&output=csv"
# (credit - https://stackoverflow.com/questions/24255472/download-export-public-google-spreadsheet-as-tsv-from-command-line)

import csv
import random
import time
import random
import signal
import os

update_score=False
CHANNELS=32
channelStates=[]
eventTimes=[]
eventIndexes=[]
lastCycleTime = 0

def clearEventTimes():
	global eventTimes
	for i in range(CHANNELS):
		eventTimes.append([])

def clearChannelStates():
	global channelStates
	for i in range(CHANNELS):
		channelStates.append(0)

def clearEventIndexes():
	global eventIndexes
	for i in range(CHANNELS):
		eventIndexes.append(0)

script_dir = os.path.split(os.path.realpath(__file__))[0]
curl = 'curl --connect-timeout 5 -m 10 -L "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1797776547&single=true&output=csv"'
temp_filename = "\"" + script_dir + "/data/score_temp.csv" +  "\""
filename = "\"" + script_dir + "/data/score.csv" +  "\""
cmd = curl+" > "+temp_filename

def setLightOn(channel):
	global channelStates
	channelStates[channel] = 1

def setLightOff(channel):
	global channelStates
	channelStates[channel] = 0

def updateCSV():
	update = -1
	try:
		update = os.system(cmd)
		print(update)
	except:
		print("Couldn't update sheet")

	if ( update == 0 ):
		os.system("mv "+temp_filename+" "+filename)
	else:
		os.system("rm "+temp_filename)
		print("curl completed with a non-zero exit status")

def openCSV():
	with open( script_dir + "/data/score.csv",'rt') as f:
		reader = csv.reader(f)
		behaviors=[]
		for row in reader:
			index=0
			times=[]
			variations=[]
			offset_variation=0
			for item in row:
				temp = -1.0

				if item: # execute if string isn't empty
					try: # convert appropriate strings to float
						temp=float(item)
					except:
						pass

					if (temp != -1): # test if a conversion happened
						if (index == 0):
							offset_variation=(temp)
						elif (index % 2 == 1):
							times.append(temp)
						else:
							variations.append(temp)
						index += 1
			behaviors.append(list([times,variations,offset_variation]))
	return behaviors

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	os._exit(0)

def printBehavior(behavior):
	for i, timing in enumerate(behavior):
		print(behavior[i])

def timing():

	global eventTimes
	global eventIndexes

	for c in range(CHANNELS):
		if eventTimes[c]:
			if (time.time() > eventTimes[c][0]):
				eventIndexes[c]^=1
				if (eventIndexes[c] == 1):
					setLightOn(c)
				elif (eventIndexes[c] == 0):
					setLightOff(c)
				eventTimes[c]=eventTimes[c][1:]
				if (len(eventTimes[c])==0):
					setLightOff(c)
					eventIndexes[c]^=1


def generateTimings(behavior):
	times=[]
	startTime=time.time()
	offset = random.uniform(-behavior[2],behavior[2])
	for t in range(len(behavior[0])):
		eventTime = startTime + offset + behavior[0][t] + random.uniform(-behavior[1][t],behavior[1][t])
		times.append(eventTime)
	return times

def main():

	clearEventTimes()
	clearChannelStates()
	clearEventIndexes()

	if update_score: updateCSV()

	behaviors = openCSV()

	global eventIndexes
	global eventTimes
	global lastCycleTime

	while True:

		cycleTime = int(time.time()) % 90 
		print("--->"+str(cycleTime)+str(channelStates),end='\r')
		if( cycleTime == 0 and cycleTime != lastCycleTime):
			startTime = time.time()
			for c in range(CHANNELS):
				index = random.randint(0,len(behaviors)-1)
				behavior = behaviors[ index ]
				eventTimes[c]+=generateTimings(behavior)
		timing()
		lastCycleTime=cycleTime
		time.sleep(.1)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()