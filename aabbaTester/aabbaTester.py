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

syllableList = ["B","C","D","F","G","H","K","L","M","O","P","Q","S","T",
					"U","W","X","Y","4","5","6","r","8","9","@","#","$",
					"(",")","`","-","+","=","'",":",";",",",">",".","f","g",
					"h","j","k","l"]

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
	if lineX[-2:] == lineY[-2:] : #check for last two phonemes matching
		return 1
	elif lineX[-1:] == lineY[-1:] : #check for last phonememe matching
		return 0

def getSyllableCount(line) :
	syllableCount = 0
	for i in range(0,len(line)) :
		if line[i:i+1] in syllableList :
			syllableCount = syllableCount + 1
	return syllableCount

def lastLineMatchesFirstTwo(line1,line2,line5) :
	if (
		linesRhyme(line1,line5) == 0 or 
		linesRhyme(line1,line5) == 1 or
		linesRhyme(line2,line5) == 0 or
		linesRhyme(line2,line5) == 1
	   ):
		return True
	else : return False

def aabbaTest(line1, line2, line3, line4, line5) :
	#get average syllable count for line1, line2, and line5
	aSyllAverage = ((getSyllableCount(line1) 
					+ getSyllableCount(line2) 
					+ getSyllableCount(line5))/3)
	
	#get average syllable count for line3, and line4
	bSyllAverage = ((getSyllableCount(line3) 
					+ getSyllableCount(line4))/2)
	
	if (
		aSyllAverage > bSyllAverage and # this ensures distinct A lines and B lines exist
		getSyllableCount(line1) > getSyllableCount(line3) and # these two ensure the AABBA form
		getSyllableCount(line2) > getSyllableCount(line4)
		):
		#print(convertCharLineToWords(line1))# + ', syllCount: ' + str(getSyllableCount(line1)))
		#print(convertCharLineToWords(line2))# + ', syllCount: ' + str(getSyllableCount(line2)))
		#print(convertCharLineToWords(line3))# + ', syllCount: ' + str(getSyllableCount(line3)))
		#print(convertCharLineToWords(line4))# + ', syllCount: ' + str(getSyllableCount(line4)))
		#print(convertCharLineToWords(line5))# + ', syllCount: ' + str(getSyllableCount(line5)))
		#print('these 5 lines have the syllabic form of aabba^' + '\n')
		return True
	else : return False

def totalAABBATest(fileName) :
	#limFile = open('allLinesClean_5.txt', 'r')
	limFile = open(fileName, 'r')

	i = 0

	linesToTest = []

	numLims = 0
	numAABBAs = 0
	aabbasSatisfyingCond2 = 0

	for line in limFile :
		line = line.strip()
		if line != '\n' and line != '' :
			i += 1
			linesToTest.append(line)

			if i == 5 : # send every 5 lines in
				numLims += 1
				if aabbaTest(linesToTest[0], 
						  linesToTest[1],
						  linesToTest[2],
						  linesToTest[3],
						  linesToTest[4]) :
					numAABBAs +=1
					if lastLineMatchesFirstTwo(linesToTest[0],
											   linesToTest[1],
											   linesToTest[4]) :
						#print('and here is a limerick satisfying question 2')
						#print('////////////////////////////////////////////')
						aabbasSatisfyingCond2 += 1
				i = 0
				linesToTest = []

	limFile.close()

	statisticsF.write('stats for ' + fileName)
	statisticsF.write('\n')
	
	statisticsF.write('numAABBAs/numLims: ')
	statisticsF.write(str(numAABBAs/numLims))
	statisticsF.write('\n')
	
	statisticsF.write('aabbasSatisfyingCond2/numAABBAs: ')
	statisticsF.write(str(aabbasSatisfyingCond2/numAABBAs))
	statisticsF.write('\n')
	
statisticsF = open('aabbaStats.txt', 'w')	

totalAABBATest('lstmIn.txt')

for i in range(3,11) :
	print(i)
	fileNameToPass = 'lstm_output_' + str(i) + '.txt'
	totalAABBATest(fileNameToPass)
	
statisticsF.close()