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

lstmFile = open("lstm_output_6.txt", "r")
overfittedLines = open("overfittedLines.txt","w")
originalLines = open("originalLines.txt", "w")

alreadyMatched = []

numLines = 0
numMatches = 0
skipLines = 1

def convertCharLineToWords(line):
	convertedLine = ""
	words = line.split()
	for elem in words :
		if elem in ch2wrdsDict :
			convertedLine = convertedLine + ch2wrdsDict[elem]+" "
		else :
			convertedLine = convertedLine + "DNF " #seq2seq output would go here
	return convertedLine


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
			consecutiveOGLinesChecker = 0
			
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
								consecutiveOGLinesChecker = 0
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
				consecutiveOGLinesChecker += 1
				originalLines.write(convertCharLineToWords(lineX))
				originalLines.write("\n")
				if consecutiveOGLinesChecker == 2 :
					print("consecutive original lines found")
originalLines.close()			
overfittedLines.close()
lstmFile.close()

#write actual statistic to separate file
overfitPercentage = numMatches/numLines
writeF = open("overfitPercentage.txt", "w")
writeF.write("overfitPercentage: ")
writeF.write(str(overfitPercentage))
writeF.close()