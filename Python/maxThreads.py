#!/usr/bin/python3

from threading import Timer

count = 0

def callback(number):
	global count
	count -= 1
	print(" [-] Thread finished: "+str(number))

def main():
	global count
	while True:
		count+=1
		Timer(1, callback,[count]).start()
		print(" [+] Threads running: "+str(count))

main()