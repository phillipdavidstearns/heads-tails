#!/usr/bin/python3

import csv
from threading import Timer
import random
import time
import random
import signal
import os

t0 = 0.0
Timers = []

def setLightOn(channel):
	print("Channel: " + str(channel) + ", Light is ON @: "+str(time.time() - t0))

def setLightOff(channel):
	print("Channel: " + str(channel) + ", Light is OFF @: "+str(time.time() - t0))

def openCSV():
	with open('./data/score_draft.csv','rt') as f:
		reader = csv.reader(f)
		behaviors=[]
		for row in reader:
			index=0
			times=[]
			variations=[]

			for item in row:
				temp = -1.0

				if item: # execute if string isn't empty
					try: # convert appropriate strings to float
						temp=float(item)
					except:
						pass

					if (temp != -1): # test if a conversion happened

						if (index % 2 == 0):
							times.append(temp)
						else:
							variations.append(temp)
						index += 1

			behaviors.append(list([times,variations]))
	return behaviors

def keyboardInterruptHandler(signal, frame):
	print()
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	os._exit(0)

def main():

	global t0
	global Timers

	Timers = []

	print("hello!")

	behaviors = openCSV()
	whichChannel= random.randint(0,31)
	behavior = behaviors[random.randint(0,len(behaviors)-1)]

	for i, timing in enumerate(behavior):
		print(behavior[i])

	for j in range(len(behavior[0])):
		delay = behavior[0][j] + random.uniform(0,behavior[1][j])
		if (j % 2 == 0):
			Timers.append(Timer(delay,setLightOn,[whichChannel]))
		else:
			Timers.append(Timer(delay,setLightOff,[whichChannel]))

	t0 = time.time()
	for t in Timers:
		t.start()

signal.signal(signal.SIGINT, keyboardInterruptHandler)

main()