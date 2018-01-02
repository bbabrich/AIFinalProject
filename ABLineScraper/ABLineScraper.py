# open up our files
readF = open("limsAsChars.txt", "r")
writeA = open("ALines.txt", "w")
writeB = open("BLines.txt", "w")

limerick = []
for line in readF :
	# print(len(line))
	if len(line) >= 3 : # hit a real line
		limerick = limerick + [line] # so add that line to our current limerick
	elif len(line) < 3 : # hit an empty line
		i = 1 # dummy indexing variable
		GLen = 0 # GLen becomes either ALen or BLen depending on length of first line
		# This is because (due to formatting issues) sometimes a B line is first
		for l in limerick :
			if i == 1 :
				GLen = len(l) # grab length of first line
			if GLen >= 24 : # first line is an A line
				if abs(len(l) - GLen) > 6 and len(l) < GLen : # line is a B line
					writeB.write(l)
					#writeB.write("\n")
				else : # line is an A line
					writeA.write(l)
					#writeA.write("\n")
			else : # first line is a B line
				if abs(len(l) - GLen) > 6 and len(l) > GLen : # line is an A line
					writeA.write(l)
					#writeA.write("\n")
				else : # line is a B line
					writeB.write(l)
					#writeB.write("\n")
			i = i + 1
		limerick = [] # reset our current limerick
# close our files
readF.close()
writeA.close()
writeB.close()