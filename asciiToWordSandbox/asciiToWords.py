#create a dictionary for ascii to phoneme
phon2charF = open("phonToCharDict.txt","r")
ch2phDict = {}

for line in phon2charF :
	line = line.strip()
	if line != "" and line[0:2] != "IY0":
		keyAndValue = line.split("-")
		ch2phDict[keyAndValue[0]] = keyAndValue[1]
	ch2phDict["IY0"] = "-" #it was silly to use "-" as one of our chars...

'''
print("char to phone dictionary")
for key in ch2phDict :
	print(key + " " + ch2phDict[key])
phon2charF.close()
'''

#create a dictionary for phonemes to words
chars2phonsF = open("cmuDict.txt","r")

phnms2wrdsDict = {}

for line in chars2phonsF :
	line = line.strip()
	keyAndValue = line.split(" ")
	key = keyAndValue[0]
	phnms2wrdsDict[key] = keyAndValue[1:]

'''
print("phonemes to words dictionary")
for key in phnms2wrdsDict :
	print(key + ", " + " ".join(phnms2wrdsDict[key]))
chars2phonsF.close()
'''

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

'''
print("words to chars dictionary")
for key in ch2wrdsDict :
	print(key + ", " + ch2wrdsDict[key])
'''

#let's test this dictionary on our original lines
originalLinesF = open("originalLines.txt", "r")

for line in originalLinesF :
	words = line.split()
	for elem in words :
		if elem in ch2wrdsDict :
			print(ch2wrdsDict[elem]+" ", end="")
		else :
			print("DNF ", end="")
	print("")
	
originalLinesF.close()