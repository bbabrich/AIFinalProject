#run stats on lstm output 3-10 (the ones with char output)
for j in range(3,10) :
	fileName = "lstm_output_"+str(j)+".txt"
	# open up our file
	readF = open(fileName, "r")
	skipLines = 1

	checkLine = "xx"
	checkSlant = "xx"
	checkSyllable = 0

	weakRhymes = 0
	strongRhymes = 0
	slantRhymes = 0
	syllableMatches = 0
	validLines = 0

	syllableList = ["B","C","D","F","G","H","K","L","M","O","P","Q","S","T",
					"U","W","X","Y","4","5","6","r","8","9","@","#","$",
					"(",")","`","-","+","=","'",":",";",",",">",".","f","g",
					"h","j","k","l"]

	#gather stats
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
				skipLines = 3;

			if skipLines <= 0 : #we hit a line we want to check for rhyming with
				validLines = validLines + 1
				line = line.rstrip() # strip lines of trailing spaces/newlines
				checkLine = checkLine.rstrip()

				#strong/weakrhyme check
				if line[-2:] == checkLine[-2:] : #check for last two phonemes matching
					#print(line)
					#print(checkLine)
					#print(line[-2:])
					#print(checkLine[-2:])
					#print("strong rhyme^")
					strongRhymes = strongRhymes + 1 
				elif line[-1:] == checkLine[-1:] : #check for last phonememe matching
					#print(line)
					#print(checkLine)
					#print(line[-1:])
					#print(checkLine[-1:])
					#print("weak rhyme^")
					weakRhymes = weakRhymes + 1

				#check for slant rhymes here
				slantSyllable = "yy"
				#print("LINE: "+line)
				for i in range(1, len(line)+1) :
					#print(line[-i])
					#start at the end of the line
					if line[-i] == " "  or line[-i] in syllableList:#check for matching syllables
						if line[-i] in syllableList: 
							#print("syllable found in last word: "+line[-i])
							slantSyllable = line[-i]
						break;
				if slantSyllable == checkSlant :
					#print("checkLine: " + checkLine)
					#print("line: " + line)
					#print("each have a slant rhyme count of: ", slantSyllable)
					slantRhymes +=1

				#count and check syllables here
				syllableCount = 0

				#print("line: "+ line)
				for i in range(0,len(line)) :
					# print(line[i:i+1]+" ", end='')
					if line[i:i+1] in syllableList :
						syllableCount = syllableCount + 1
				# print("\n")
				if syllableCount == checkSyllable :
					#print("checkLine: " + checkLine)
					#print("line: " + line)
					#print("each have an equal syllable count of: ", syllableCount)
					syllableMatches = syllableMatches + 1

				checkSlant = slantSyllable
				checkLine = line
				checkSyllable = syllableCount

	writeF = open("rhymeAndSyllableStats.txt","a+")

	#append stats to rhymeAndSyllableStats.txt
	writeF.write(fileName)
	writeF.write("\n")

	writeF.write("percentage of weak rhymes: ")
	writeF.write(str(weakRhymes/(validLines-1) *100))
	writeF.write("\n")

	writeF.write("percentage of strong rhymes: ")
	writeF.write(str(strongRhymes/(validLines-1) *100))
	writeF.write("\n")

	writeF.write("percentage of matching syllable counts: ")
	writeF.write(str(syllableMatches/(validLines-1) *100))
	writeF.write("\n")

	writeF.write("percentage of slant rhymes: ")
	writeF.write(str(slantRhymes/(validLines-1) *100))
	writeF.write("\n")
	writeF.write("\n")

	#print("percentage of weak rhymes: ",weakRhymes/(validLines-1) *100)
	#print("percentage of strong rhymes: ",strongRhymes/(validLines-1) *100)
	#print("percentage of matching syllable counts: ", syllableMatches/(validLines-1) *100)
	#print("percentage of slant rhymes: ", slantRhymes/(validLines-1) *100)
	readF.close()
	writeF.close()