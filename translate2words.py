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
numWords=0
total = 0
output = open("output1.txt","r")
t = open('2wordsOutput1.txt','w')
for line in output:
    if ("Iteration" in line) or ("Epoch" in line) or ("-----" in line):
        t.write(line)
    elif "loss" not in line:
        string = line.split(' ')
        string = [x for x in string if (x != '' and x != '\n')]
        for word in string:
            total = total+1
            if word in ascii2wordDict:
                t.write(ascii2wordDict[word]+' '),
                numWords = numWords+1
            else:
                t.write("wtf"+' '),
        t.write('\n')

t.write("STATS: ")
percent = numWords/total
t.write(str(percent))

