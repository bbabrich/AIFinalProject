#IGNORING

'''
#create a dictionary for phoneme sequence to word
phon2word = open("cmuDict.txt","r")
ph2wordDict = {}
for line in phon2word:
    i = line.index(' ')
    phStr = line[i+2:len(line)]
    phList = phStr.split(' ')
    last = len(phList)
    phList[last-1] = phList[last-1][0:len(phList[last-1])-1]    
    wordChars = ''
    for ph in phList:
        wordChars = wordChars + ph2chDict[ph]
    data=[wordChars, line[0:i]]
    ph2wordDict[data[0]] = data[1]
print(ph2wordDict['2k'])
'''
    


#create a dictionary for ascii to phoneme
# and phoneme to ascii
phon2char = open("phonToCharDict.txt","r")
ph2chDict = {}
ch2phDict = {}
ch2phDict['\n'] = '\n'
ph2chDict[''] = ''
for line in phon2char  :
    if '-' in line:
        data = line.rstrip()
        data = data.split('-')
        if not data[1]:
            data[1] = '-'
            data.pop()
        else:
            data[1] = data[1][0]
        ph2chDict[data[0]] = data[1]
        ch2phDict[data[1]] = data[0]


#create a dictionary for word to phoneme
    #and dictionary for ascii to word
phon2word = open("cmuDict.txt","r")
word2phDict = {}
ascii2wordDict = {}
for line in phon2word:
    l = line.rstrip()
    i = l.index(' ')
    phStr = l[i+2:len(l)]
    phList = phStr.split(' ')
    last = len(phList)
    phList[last-1] = phList[last-1][0:len(phList[last-1])]
    word2phDict[l[0:i]] = phList
    wordChars = ''
    #For fixing dictionary
    #print( l[0:i])
    #print(phList)
    for ph in phList:
        wordChars = wordChars + ph2chDict[ph]
    data=[wordChars, l[0:i]]
    ascii2wordDict[data[0]] = data[1]


#ascii characters to phonemes
'''
#Grab output from lstm
output = open("snippet.txt","r")
for line in output:
    for ch in line:
        if ch == ' ':
            print(' ', end = '')
        else:
            if ch in ch2phDict:
                print(ch2phDict[ch],end = '')
            else:
                print("WTFUCK", end = '')
    print(' ')
'''





#ascii sequence to word
#Grab output from lstm
overFit50 = 0
overFit60 = 0
overFit70 = 0
overFit80 = 0
overFit90 = 0
overFit95 = 0
overFit96 = 0
overFit97 = 0
overFit98 = 0
overFit99 = 0
overFit100 = 0
total = 0
seed = 0

corpus = open('limToCharPhons.txt', 'r')
output = open("output5.txt","r")
for line in output:
    #per is the percent of words in line that match the words in one line of the limerick corpus
    per = 0
    if ("Iteration" not in line) and ("Epoch" not in line) and ("-----" not in line) and ("loss" not in line) and (not line.isspace()):
        #total number of lines in output
        total = total+1
        print(total)
        check = True
        corpus.seek(0)
        for limLine in corpus:
            #print(limLine)
            if not limLine.isspace():
                limLine = limLine.rstrip()
                #if word is in limLine
                numWords = 0
                #tot is the total number of words in line
                tot = 0

                if check:
                    #print("checking")
                    words = line.split()
                    limWords = limLine.split()
                    #print(words,limWords)
                    if (len(words)>=6) and (len(limWords)>=6):
                        stem = True
                        for x in range(0,5):
                            if words[x] != limWords[x]:
                                stem = False
                        if stem:
                            seed = seed+1
                            check = False
                            
                #to check how much a line in the output matches up with a line in the corpus    
                for word in line:
                    tot = tot+1
                    if word in limLine:
                        numWords = numWords + 1
                curPer = numWords/tot
                if curPer>per:
                    per = curPer
                    
    if per>0.95:
        overFit95 = overFit95 + 1
    if per>0.9:
        overFit90 = overFit90 + 1
    if per>0.8:
        overFit80 = overFit80 + 1
    if per>0.7:
        overFit70 = overFit70 + 1
    if per>0.6:
        overFit60 = overFit60 + 1
    if per>0.5:
        overFit50 = overFit50 + 1
    if per>0.96:
        overFit96 = overFit96 + 1
    if per>0.97:
        overFit97 = overFit97 + 1
    if per>0.98:
        overFit98 = overFit98 + 1
    if per>0.99:
        overFit99 = overFit99 + 1
    if per>1.0:
        overFit100 = overFit100 + 1
    
    
print("STATS: ")
percent50 = overFit50/total
print("0.5 Match")
print(str(percent50))
percent60 = overFit60/total
print("0.6 Match")
print(str(percent60))
percent70 = overFit70/total
print("0.7 Match")
print(str(percent70))
percent80 = overFit80/total
print("0.8 Match")
print(str(percent80))
percent90 = overFit90/total
print("0.9 Match")
print(str(percent90))
percent95 = overFit95/total
print("0.95 Match")
print(str(percent95))
percent96 = overFit96/total
print("0.96 Match")
print(str(percent96))
percent97 = overFit97/total
print("0.97 Match")
print(str(percent97))
percent98 = overFit98/total
print("0.98 Match")
print(str(percent98))
percent99 = overFit99/total
print("0.99 Match")
print(str(percent99))
percent100 = overFit100/total
print("1.00 Match")
print(str(percent100))


print("Seed Match:")
per = seed/total
print(str(per))
