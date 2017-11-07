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

limerickF = open("sixLimericks.txt", "r")
writeF = open("limToCharPhons.txt", "w")

'''
for line in limerickF :
	outStr = ""
	word = ""
	str = ""
	phonStr = ""
	j = 0;
	for i in range(0, len(line)) :
		if line[i] != " " and line[i] != '\n':
			str = str + line[i:i+1]
		else :
			word = str[j:i]
			# Search for word in cmuDict and return phenomic version
			cmuDictF = open("cmuDict.txt", "r")
			for lineL in cmuDictF :
				phonFind = ""
				for k in range(0, len(lineL)):
					if lineL[k] != " ":
						# print(lineL[k])
						phonFind = phonFind + lineL[k]
					else :
						break
				if word.upper() == phonFind :
					phonStr = lineL[k:len(lineL)]
					# print(phonFind + ", phonemic: " + phonStr)
			cmuDictF.close()
			phonStr = phonStr[0:len(phonStr)-1]
			outStr = outStr + phonStr + "_"
			# print("phonStr: " + phonStr)
			# print("word: " + word)
			j = i+1;
			str = str + " ";
	# print(outStr)
	writeF.write(outStr)
	writeF.write('\n')
	print("line processed into : " + outStr)
'''
limerickF.close()
writeF.close()
