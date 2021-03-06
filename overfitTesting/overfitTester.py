#B Chase Babrich
#This file checks LSMT output for overfitting
#if a line is not "overfitted", it is converted to words and written to a file

#//////////////////////ASCII TO WORD CONVERSION TOOLS//////////////////////////////////

#create a dictionary for ascii to phoneme
phon2charF = open("phonToCharDict.txt","r")
ch2phDict = {}

for line in phon2charF :
	line = line.strip()
	if line != "" and line[0:2] != "IY0":
		keyAndValue = line.split("-")
		ch2phDict[keyAndValue[0]] = keyAndValue[1]
	ch2phDict["IY0"] = "-" #it was silly to use "-" as one of our chars...

#create a dictionary for phonemes to words
chars2phonsF = open("cmuDict.txt","r")

phnms2wrdsDict = {}

for line in chars2phonsF :
	line = line.strip()
	keyAndValue = line.split(" ")
	key = keyAndValue[0]
	phnms2wrdsDict[key] = keyAndValue[1:]

#merge those two dictionaries into an ascii to words dictionary
ch2wrdsDict = {}

for key in phnms2wrdsDict :
	#print(" ".join(phnms2wrdsDict[key])[1:])
	del phnms2wrdsDict[key][0] #get rid of empty "" spot at the beginning (?)
	val = ""
	for elem in phnms2wrdsDict[key] :
		#print(ch2phDict[elem].strip())
		val = val +  ch2phDict[elem].strip()
	ch2wrdsDict[val] = key

#//////////////////////OVERFIT TESTING STARTS HERE//////////////////////////////////
def overfitTest(outputNum) :
	lstmFileName = "lstm_output_"+str(outputNum)+".txt"
	lstmFile = open(lstmFileName, "r")
	
	allLinesCleanFileName = "allLinesClean_"+str(outputNum)+".txt"
	allLinesClean = open(allLinesCleanFileName, "w")
	
	overfittedLinesFileName = "overfittedLines_"+str(outputNum)+".txt"
	overfittedLines = open(overfittedLinesFileName,"w")
	
	originalLinesFileName = "originalLines_"+str(outputNum)+".txt"
	originalLines = open("originalLines.txt", "w")

	rhymingLinesFileName = "rhymingLines_"+str(outputNum)+".txt"
	rhymingLines = open(rhymingLinesFileName, "w")
	
	alreadyMatched = []

	numLines = 0
	numMatches = 0
	skipLines = 1

	strongRhymes = 0
	weakRhymes = 0

	numOfOriginalLines = 0
	numOfConsecutiveOGLines = 0
	numOfOriginalRhymes = 0

	consecutiveOGLinesChecker = 0

	checkLine = "xx"

	#takes in a line in ASCII format
	#returns a line in human words
	#write 'DNF' for words which are not in the CMU dictionary
	def convertCharLineToWords(line):
		convertedLine = ""
		words = line.split()
		for elem in words :
			if elem in ch2wrdsDict :
				convertedLine = convertedLine + ch2wrdsDict[elem]+" "
			else :
				convertedLine = convertedLine + "DNF" #seq2seq output would go here
		return convertedLine

	def linesRhyme(lineX, lineY) :
		if lineX[-2:] == lineY[-2:] : #check for last two phonemes matching
			return 1
		elif lineX[-1:] == lineY[-1:] : #check for last phonememe matching
			return 0

	#check each line from output for overfitting
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
				allLinesClean.write(lineX)
				allLinesClean.write("\n")
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

						#here is where the actual overfit checking happens
						#for 50% of the output line, we see if we can find
						#a matching sequence of strings in the input
						#if we do, we stop looking (foundBool)
						streak = 0
						matchingWords = []
						for i in range(0,n) :
							k = i
							for j in range(0,len(yWords)):
								if xWords[k] == yWords[j] and k <= n:
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
									consecutiveOGLinesChecker = 0
									checkLine = "xx"
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
				if not foundBool : #we've found an originally written line
					numOfOriginalLines += 1
					consecutiveOGLinesChecker += 1
					if consecutiveOGLinesChecker == 1 : checkLine = lineX
					originalLines.write(convertCharLineToWords(lineX))
					originalLines.write("\n")
					#print(consecutiveOGLinesChecker)
					if consecutiveOGLinesChecker == 2 : #we've found two consecutively written original lines
						numOfConsecutiveOGLines += 1
						#print("consecutive original lines found")
						#print(checkLine)
						#print(lineX)
						if linesRhyme(checkLine, lineX) == 1:
							#print(convertCharLineToWords(checkLine))
							#print(convertCharLineToWords(lineX))
							#print("strong original rhyme found^")
							
							rhymingLines.write(convertCharLineToWords(checkLine))
							rhymingLines.write("\n")
							
							rhymingLines.write(convertCharLineToWords(lineX))
							rhymingLines.write("\n")
							
							rhymingLines.write("strong original rhyme found^")
							rhymingLines.write("\n")
							
							strongRhymes = strongRhymes + 1
							numOfOriginalRhymes += 1
						if linesRhyme(checkLine, lineX) == 0:
							#print(convertCharLineToWords(checkLine))
							#print(convertCharLineToWords(lineX))
							#print("weak original rhyme found^")
							
							rhymingLines.write(convertCharLineToWords(checkLine))
							rhymingLines.write("\n")
							
							rhymingLines.write(convertCharLineToWords(lineX))
							rhymingLines.write("\n")
							
							rhymingLines.write("weak original rhyme found^")
							rhymingLines.write("\n")
							
							weakRhymes = weakRhymes + 1
							numOfOriginalRhymes += 1
						checkLine = lineX
						consecutiveOGLinesChecker = 0
	
	#close all of our files
	originalLines.close()			
	overfittedLines.close()
	lstmFile.close()
	rhymingLines.close()
	allLinesClean.close()

	#write actual statistic to separate file
	overfitPercentage = numMatches/numLines
	writeF = open("overfitPercentages.txt", "a+")
	
	writeF.write("overfitting statistics for output "+ str(outputNum))
	writeF.write("\n")
	
	writeF.write("overfitPercentage: ")
	writeF.write(str(overfitPercentage))
	writeF.write("\n")
	
	writeF.write("numOfOriginalLines/numLines: ")
	writeF.write(str(numOfOriginalLines/numLines))
	writeF.write("\n")

	writeF.write("numOfConsecutiveOGLines/numOfOriginalLines: ")
	writeF.write(str(numOfConsecutiveOGLines/numOfOriginalLines))
	writeF.write("\n")

	writeF.write("numOfOriginalRhymes/numOfConsecutiveOGLines: ")
	writeF.write(str(numOfOriginalRhymes/numOfConsecutiveOGLines))
	writeF.write("\n")	
	
	writeF.close()

	#print("numOfOriginalLines/numLines: "+str(numOfOriginalLines/numLines))
	#print("numOfConsecutiveOGLines/numOfOriginalLines: "+str(numOfConsecutiveOGLines/numOfOriginalLines))
	#print("numOfOriginalRhymes/numOfConsecutiveOGLines: "+str(numOfOriginalRhymes/numOfConsecutiveOGLines))

#main loop which runs over all seven files
#overfitTest(6)
#print("yes")

for i in range(3,6) :
	print(i)
	overfitTest(i)
