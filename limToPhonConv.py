# create a dict data structure for CMUDict for fast access [~O(1)]
cmuDictF = open("cmuDict.txt", "r")
phonDict = {}
for line in cmuDictF :
	phonKey = ""
	for k in range(0, len(line)):
		if line[k] != " ":
			phonKey = phonKey + line[k]
		else :
			break
	phonVal = line[k+2:len(line) - 1] # +/- are for spaces/newline chars
	phonDict[phonKey] = phonVal
	
# a few test prints of the newly created dictionary
'''
print(phonDict["A"])
print(phonDict["AARONSON"])
print(phonDict["STAUFFER"])
for k in phonDict :
	print(k)
'''
cmuDictF.close()

# do the same for the phonemes to single characters dictionary
phonCharDictF = open("phonToCharDict.txt", "r")
charDict = {}
for line in phonCharDictF :
	charKey = ""
	for k in range(0, len(line)):
		if line[k] != "-":
			charKey = charKey + line[k]
		else :
			break
	charVal = line[k+1]
	charDict[charKey] = charVal

# a test print to check phoneme to character dictionary is set up properly
'''
for k,v in charDict.items() :
	print(k,v)	
'''
phonCharDictF.close()

# CONVERSION FROM LIMERICKS TO CHARS BEGINS HERE
# for each word w in the limerick :
#		retrieve w's corresponding phoneme p
#		for each string in p
#			retrieve corresponding char c
#		write a string s consisting of all c found in above loop to output file
# file reading assumes that
#		there are end of line characters in input file
# 		assumes there is a blank line at the very end of the input file

limerickF = open("limerickCorpus.txt", "r")
writeF = open("limToCharPhons.txt", "w")
missingWordsF = open("missingWords.txt", "w")

for line in limerickF :
	j = 0;
	str=""
	outLine = ""
	for i in range(0, len(line)) :
		outStr = ""
		# split up lines into words based on spaces
		# do not consider non-alphabetical characters
		if (line[i] != " " and line[i] != "\n" and line[i] != "," and line[i] != "’"
			and line[i] != "“" and line[i] != "”" and line[i] != "!" and line[i] != ";" 
			and line[i] != "\"" and line[i] != "?" and line[i] != "." and line[i] != ":"): 
			str = str + line[i]
		else :
			# word within line is found
			word = str[j:i].upper()
			if word != "" : # take care of pesky end of line characters
				# print(word)
				# word's corresponding phoneme is retreived
				if word in phonDict : # check if word is in dictionary
					phoneme = phonDict[word]
					# print(phoneme)
					# phoneme is broken up into individual strings
					phStr = ""
					# print(phoneme)
					for k in range(0,len(phoneme)) :
						if phoneme[k] != " " :
							phStr = phStr + phoneme[k]
							if k == len(phoneme) - 1 : # - 1 due to indices starting at 0?
								# print(phStr)
								outStr = outStr + charDict[phStr]
						else :
							outStr = outStr + charDict[phStr]
							phStr = ""
							k = k + 1
				else : # if word is not in dictionary write it to out file
					outStr = word # do nothing with word (for the time being)
					missingWordsF.write(word)
					missingWordsF.write("\n")
			j = i+1;
			str = str + " ";
			outLine = outLine + outStr + " " 
	# print(outLine)
	writeF.write(outLine)
	writeF.write("\n")
missingWordsF.close()
limerickF.close()
writeF.close()
