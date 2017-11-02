#assumes there end of line characters

limerickF = open("limerick.txt", "r")

writeF = open("phonLim.txt", "w")

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
			phonStr = phonStr[0:len(phonStr)-2
			outStr = outStr + phonStr + "_"
			# print("phonStr: " + phonStr)
			# print("word: " + word)
			j = i+1;
			str = str + " ";
	print(outStr)
limerickF.close()
writeF.close()