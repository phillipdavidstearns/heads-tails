import time
resynchFlag=True

def main():
	global resynchFlag
	while True:
		resynchTime = int(time.time()) % 30
		if( resynchTime == 0 and resynchFlag):
			resynchFlag=False
			print("clearflag")
		elif(resynchTime != 0 and not resynchFlag):
			resynchFlag=True
			print("resetflag")
		time.sleep(.1)

main()