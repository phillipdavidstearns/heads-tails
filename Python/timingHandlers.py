import subprocess
import time

INCREMENT = 1/120.0
tzOffset = -5 * 3600
dotOffset = 0 # based on the start of Phase B @ 51 seconds in the cycle starting + 28 past midnight
deviation = 0
power_line_time=time.time()

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