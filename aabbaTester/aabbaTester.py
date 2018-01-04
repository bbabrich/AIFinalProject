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
	del phnms2wrdsDict[key][0] #get rid of empty "" spot at the beginning (?)
	val = ""
	for elem in phnms2wrdsDict[key] :
		val = val +  ch2phDict[elem].strip()
	ch2wrdsDict[val] = key

def convertCharLineToWords(line):
		convertedLine = ""
		words = line.split()
		for elem in words :
			if elem in ch2wrdsDict :
				convertedLine = convertedLine + ch2wrdsDict[elem]+" "
			else :
				convertedLine = convertedLine + ' ' + elem + ' ' #seq2seq output would go here
		return convertedLine

def linesRhyme(lineX, lineY) :
	if (lineX[-3:] == lineY[-3:] or
		lineX[-2:] == lineY[-2:] or
		lineX[-1:] == lineY[-1:] 
	   ): #check for last phonememe matching
		return True
	else : return False

syllableList = ["B","C","D","F","G","H","K","L","M","O","P","Q","S","T",
					"U","W","X","Y","4","5","6","r","8","9","@","#","$",
					"(",")","`","-","+","=","'",":",";",",",">",".","f","g",
					"h","j","k","l"]
	
def getSyllableCount(line) :
	syllableCount = 0
	for i in range(0,len(line)) :
		if line[i:i+1] in syllableList :
			syllableCount = syllableCount + 1
	return syllableCount

#part of condition 3
def firstTwoLinesMatchSecondTwo(line1,line2,line3,line4) :
	if (
		linesRhyme(line1,line3) or
		linesRhyme(line1,line4) or
		linesRhyme(line2,line3) or
		linesRhyme(line2,line4)
		):
		return True
	else : return False

# condition 2
def lastLineMatchesFirstTwo(line1,line2,line5) :
	if (
		linesRhyme(line1,line5) or 
		linesRhyme(line2,line5)
	   ): return True
	else : return False

# condition 1
def aabbaTest(line1, line2, line3, line4, line5) :
	#get average syllable count for line1, line2, and line5
	aSyllAverage = ((getSyllableCount(line1) 
					+ getSyllableCount(line2) 
					+ getSyllableCount(line5))/3)
	
	#get average syllable count for line3, and line4
	bSyllAverage = ((getSyllableCount(line3) 
					+ getSyllableCount(line4))/2)
	
	rhymeCondition = (linesRhyme(line1,line2) and 
					 linesRhyme(line1,line5) and
					 linesRhyme(line3,line4))
	
	if (
		aSyllAverage > bSyllAverage and # this ensures distinct A lines and B lines exist
		getSyllableCount(line1) > getSyllableCount(line3) and # these two ensure the AABBA form
		getSyllableCount(line2) > getSyllableCount(line4) and # as opposed to ABBAA
		rhymeCondition # this one ensures the AABBA rhyming property
		): return True
	else : return False

def linePassesFilter(line, skipLines) :
	if (
		skipLines <= 0 and
		"--------" not in line and
		"Iteration" not in line and
		"Epoch" not in line and
		"loss" not in line and
		line[0:7] != "----- d" and
		line != ""
			   ): return True
	else : return False	
	
def totalAABBATest(fileName) :
	#limFile = open('allLinesClean_5.txt', 'r')
	limFile = open(fileName, 'r')

	i = 0

	linesToTest = []

	numLims = 0
	numAABBAs = 0
	aabbasSatisfyingCond2 = 0
	aabbasSatisfyingCond3 = 0
	
	totRhymes = 0
	cleanRhymes = 0
	
	tempLine = "xx"
	
	skipLines = 0

	for line in limFile :
		line = line.strip()
		if line[0:7] == "----- G" : skipLines = 3
		skipLines -= 1
	
		if linePassesFilter(line,skipLines) :
			# rhyme testing
			if linesRhyme(line,tempLine) : totRhymes += 1
			if (
				linesRhyme(line,tempLine) and
				line.split()[-1] != tempLine.split()[-1]
			   ): 
				cleanRhymes += 1
			tempLine = line
			
			i += 1
			
			cond1 = False
			cond2 = False
			cond3 = False
			
			linesToTest.append(line)

			if i == 5 : # send every 5 lines in
				numLims += 1
				if aabbaTest(linesToTest[0], 
						  linesToTest[1],
						  linesToTest[2],
						  linesToTest[3],
						  linesToTest[4]) :
					cond1 = True
					numAABBAs +=1
					
					#test for condition two
					#i.e., does the last line's rhyme match
					#either of the first two lines'?
					if lastLineMatchesFirstTwo(linesToTest[0],
											   linesToTest[1],
											   linesToTest[4]) :
						#print('and here is a limerick satisfying question 2')
						#print('////////////////////////////////////////////')
						aabbasSatisfyingCond2 += 1
						cond2 = True
					
					#test for condition three
					#i.e., does the middle BB rhyme differ from the A rhyme
					#further, the B lines themselves must rhyme
					if ((not firstTwoLinesMatchSecondTwo(linesToTest[0],
												   linesToTest[1],
												   linesToTest[2],
												   linesToTest[3])) and 
						linesRhyme(linesToTest[2],linesToTest[3])
					   ):
						aabbasSatisfyingCond3 += 1
						cond3 = True
					
					if cond1 and cond2 and cond3 :
						print(convertCharLineToWords(linesToTest[0]))
						print(convertCharLineToWords(linesToTest[1]))
						print(convertCharLineToWords(linesToTest[2]))
						print(convertCharLineToWords(linesToTest[3]))
						print(convertCharLineToWords(linesToTest[4]))
						print('this limerick from ' + fileName + ' satisfies all three conditions ^')
				i = 0
				linesToTest = []

	limFile.close()

	statisticsF.write('AABBA stats for ' + fileName)
	statisticsF.write('\n')
	
	statisticsF.write('numAABBAs/numLims: ')
	statisticsF.write(str(numAABBAs/numLims))
	statisticsF.write('\n')
	
	statisticsF.write('aabbasSatisfyingCond2/numLims: ')
	statisticsF.write(str(aabbasSatisfyingCond2/numLims))
	statisticsF.write('\n')
	
	statisticsF.write('aabbasSatisfyingCond3/numLims: ')
	statisticsF.write(str(aabbasSatisfyingCond3/numLims))
	statisticsF.write('\n')
	
	statisticsF.write('cleanRhymes/totRhymes: ')
	statisticsF.write(str(cleanRhymes/totRhymes))
	statisticsF.write('\n')
	
statisticsF = open('aabbaStats.txt', 'w')	

totalAABBATest('lstmIn.txt')

for i in range(3,11) :
	print(i)
	fileNameToPass = 'lstm_output_' + str(i) + '.txt'
	totalAABBATest(fileNameToPass)

statisticsF.close()