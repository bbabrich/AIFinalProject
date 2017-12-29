lstmFile = open("lstm_output_6.txt", "r")

writeF = open("overfitStats.txt","w")

alreadyMatched = []

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
			
			print("LSTMOUT line: "+lineX)
			foundBool = False;
			corpusFile = open("lstmIn.txt", "r")
			for lineY in corpusFile :
				lineY = lineY.strip()
				if lineY != "" :
					xWords = lineX.split()
					yWords = lineY.split()

					#n = 50% of the number of words in lineX
					n = int(len(xWords)/2)
					#n = 2
					streak = 0

					matchingWords = []
					

					for i in range(0,n) :
						k = i
						for j in range(0,len(yWords)):
							if xWords[k] == yWords[j] :
								matchingWords.append(xWords[k])
								k += 1
								streak += 1
								#print("single word match found")
								#print("lineX: "+lineX)
								#print("lineY: "+lineY)
								#print("matchingWords: ")
								#print(matchingWords)
							else :
								matchingWords = []
								k = i
								streak = 0
							if streak == n :
								writeF.write("match found")
								writeF.write("\n")
								writeF.write("lineX: "+lineX)
								writeF.write("\n")
								writeF.write("lineY: "+lineY)
								writeF.write("\n")
								writeF.write("matchingWords: ")
								writeF.write("\n")
								writeF.write(", ".join(matchingWords))
								writeF.write("\n")
								foundBool = True;
							if foundBool : break	
				if foundBool : break
			corpusFile.close()
lstmFile.close()