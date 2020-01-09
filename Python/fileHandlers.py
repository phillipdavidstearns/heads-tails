from globalVars import *
import os
import csv

def fetchHeadlights():
	temp_filename = '"' + script_dir + '/data/headlights_temp.csv' + '"'
	filename = '"' + script_dir + '/data/headlights.csv' +  '"'
	cmd = 'curl --connect-timeout 5 -sLm 10'
	cmd += ' -o ' + temp_filename
	cmd += ' "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1716879590&single=true&output=csv"'
	update = -1

	try:
		print("[*] Requesting 'headlights.csv' data from remote server")
		update = os.system(cmd)
	except:
		print("[!] Couldn't update 'headlight.csv'")

	if ( update == 0 ):
		os.system("mv "+temp_filename+" "+filename)
		print("[+] 'headlights.csv' successfully retrieved")
	else:
		print("[!] curl completed with a non-zero exit status")
		os.system('rm '+temp_filename+' 2>/dev/null')
	return update

def loadHeadlights():
	with open( script_dir + "/data/headlights.csv",'rt') as f:
		reader = csv.reader(f)
		headlights= {}
		for row in reader:
			date=row[0]
			onTime=row[1]
			offTime=row[2]
			headlights[date]=[onTime,offTime]

	return headlights

def fetchScore():
	temp_filename = '"' + script_dir + '/data/score_temp.csv' + '"'
	filename = '"' + script_dir + '/data/score.csv' +  '"'
	cmd = 'curl --connect-timeout 5 -sLm 10'
	cmd += ' -o ' + temp_filename
	cmd += ' "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=1797776547&single=true&output=csv"'
	update = -1

	try:
		print("[*] Requesting 'score.csv' data from remote server")
		update = os.system(cmd)
	except:
		print("[!] Couldn't update 'score.csv'")

	if ( update == 0 ):
		os.system("mv "+temp_filename+" "+filename)
		print("[+] 'score.csv' successfully retrieved")
	else:
		print("[!] curl completed with a non-zero exit status")
		os.system('rm '+temp_filename+' 2>/dev/null')
	return update

def loadScore():
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

def fetchDeviation(debug=False):

	temp_filename = '"' + script_dir + '/data/deviation_temp.txt' + '"'
	filename = '"' + script_dir + '/data/deviation.txt' +  '"'
	cmd = 'curl --connect-timeout 5 -sLm 10'
	cmd += ' -o ' + temp_filename
	cmd += ' "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGp8GI85wmWP7yZaUa0EV_reKdn2yDFgRBotHnqVOfPKjek4_6JIy4lCnnp9xT9BZavKjeOy-ZYsn_/pub?gid=913901720&single=true&output=csv"'
	update = -1

	try:
		print("[*] Requesting 'deviation.txt' data from remote server")
		update = os.system(cmd)
	except:
		print("[!] Couldn't update 'deviation.txt'")

	if ( update == 0 ):
		os.system("mv "+temp_filename+" "+filename)
		print("[+] 'deviation.txt' successfully retrieved")
	else:
		print("[!] curl completed with a non-zero exit status")
		os.system('rm '+temp_filename+' 2>/dev/null')
	return update

def loadDeviation():
	with open( script_dir + "/data/deviation.txt",'rt') as f:
		deviation = f.read()
	return int(deviation)
