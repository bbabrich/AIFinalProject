# open up our file
readF = open("inputFull.txt", "r")
skipLines = 1
checkLine = "xx"
weakRhymes = 0
strongRhymes = 0
validLines = 0
for line in readF :
	skipLines = skipLines - 1
	if (
			len(line) < 40 and             # ignore epoch generation lines 
			line[0:7] != "----- d" and     # ignore diversity lines
			line != "\n" and 		       # ignore blank lines
			line != " \n" and
			line[0:9] != "Iteration" and   # ignore iteration lines
			line[0:5] != "Epoch"     	   # ignore "Epoch" lines
	   ):
		#if we hit a "generating with seed line" we want to skip the next few lines
		#i.e., we do not want to consider whether seeded lines rhyme
		if line[0:7] == "----- G" : 
			skipLines = 4;
			
		if skipLines <= 0 : #we hit a line we want to check for rhyming with
			validLines = validLines + 1
			line = line.rstrip()
			checkLine = checkLine.rstrip()
			if line[-2:] == checkLine[-2:] : #check for last two phonemes matching
				print(line)
				print(checkLine)
				print(line[-2:])
				print(checkLine[-2:])
				print("strong rhyme^")
				strongRhymes = strongRhymes + 1 
			elif line[-1:] == checkLine[-1:] : #check for last phonememe matching
				print(line)
				print(checkLine)
				print(line[-1:])
				print(checkLine[-1:])
				print("weak rhyme^")
				weakRhymes = weakRhymes + 1
			checkLine = line
print("percentage of weak rhymes: ",weakRhymes/(validLines-1) *100)
print("percentage of strong rhymes: ",strongRhymes/(validLines-1) *100)
readF.close()