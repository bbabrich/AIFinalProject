lstmFile = open("lstm_output_6.txt", "r")
overfittedLines = open("overfittedLines.txt","w")
originalLines = open("originalLines.txt", "w")

alreadyMatched = []

numLines = 0
numMatches = 0
skipLines = 1

for lineX in lstmFile :
	# LSTM OUTPUT LINE PROCESSING
	lineX = lineX.strip() # get rid of trailing spaces and newline character
	skipLines = skipLines - 1
	if lineX not in alreadyMatched :
		#if we hit a "generating with seed line" we want to skip the next few lines
		#i.e., we do not want to consider whether seeded lines rhyme
		if lineX[0:7] == "----- G" : 
			skipLines = 3
		
		if (skipLines <= 0 and
			"--------" not in lineX and
			"Iteration" not in lineX and
			"Epoch" not in lineX and
			"loss" not in lineX and
			lineX[0:7] != "----- d" and
			lineX != ""
		   ): # we hit a line we want to check for overfitting on
			numLines += 1
			foundBool = False
			
			corpusFile = open("lstmIn.txt", "r")
			for lineY in corpusFile :
				lineY = lineY.strip()
				if lineY != "" :
					xWords = lineX.split()
					yWords = lineY.split()

					#n = 50% of the number of words in lineX
					n = int(len(xWords)/2)
					#round up for odd numbers 
					if int(len(xWords)) % 2 != 0 : n += 1
					
					streak = 0

					matchingWords = []
					
					#here is where the actual overfit checking happens
					#for 50% of the output line, we see if we can find
					#a matching sequence of strings in the input
					#if we do, we stop looking (foundBool)
					for i in range(0,n) :
						k = i
						for j in range(0,len(yWords)):
							if xWords[k] == yWords[j] :
								matchingWords.append(xWords[k])
								k += 1
								streak += 1
							else :
								matchingWords = []
								k = i
								streak = 0
							if streak == n and "25/ nL|a nCp" not in " ".join(matchingWords) :
								numMatches += 1
								alreadyMatched.append(lineX)
								#write overfitted line to file
								overfittedLines.write("match found")
								overfittedLines.write("\n")
								overfittedLines.write("lineX: "+lineX)
								overfittedLines.write("\n")
								overfittedLines.write("lineY: "+lineY)
								overfittedLines.write("\n")
								overfittedLines.write("matchingWords: ")
								overfittedLines.write("\n")
								overfittedLines.write(", ".join(matchingWords))
								overfittedLines.write("\n")
								foundBool = True;
							if foundBool : break	
				if foundBool : break
			corpusFile.close()
			if not foundBool :
				originalLines.write(lineX)
				originalLines.write("\n")
originalLines.close()			
overfittedLines.close()
lstmFile.close()

#write actual statistic to separate file
overfitPercentage = numMatches/numLines
writeF = open("overfitPercentage.txt", "w")
writeF.write("overfitPercentage: ")
writeF.write(str(overfitPercentage))
writeF.close()