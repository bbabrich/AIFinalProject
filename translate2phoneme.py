
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


#ascii sequence to ph
#Grab output from lstm
output = open("snippet.txt","r")
t = open('2phon30346.txt','w')
for line in output:
    string = line.split(' ')
    string = [x for x in string if (x != '' and x != '\n')]
    for word in string:
        for ch in word:
            t.write(ch2phDict[ch]+' ')
        t.write("_"+'')
    t.write('\n')