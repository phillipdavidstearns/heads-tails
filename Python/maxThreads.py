#!/usr/bin/python3

from threading import Timer

count = 0

def callback(number):
	global count
	count -= 1
	print(" [-] Thread finished: "+str(number), end='\r')

def main():
	global count
	while True:
		count+=1
		Timer(120, callback,[count]).start()
		print(" [+] Threads running: "+str(count), end='\r')

main()