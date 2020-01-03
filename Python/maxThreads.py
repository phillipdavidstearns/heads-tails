#!/usr/bin/python3

from threading import Timer

count = 0

def callback(number):
	print(" [-] Thread finished: "+str(number), end='\r')

def main():
	global count
	while True:
		count+=1
		Timer(10, callback,[count])
		print(" [+] Thread started: "+str(count), end='\r')

main()