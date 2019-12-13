#!/usr/bin/python3

import csv

with open('/Users/phillipstearns/Dropbox/Client Work/Madeline Hollander/HeadsTails/codebase/Python/data/score_draft.csv','rt') as f:
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

# print(behaviors[-1][-1])

for i, behavior in enumerate(behaviors):
	# print(str(i)+", "+str(behavior))

	for j in range(len(behavior[0])):
		print(behavior[0][j])
		print(behavior[1][j])