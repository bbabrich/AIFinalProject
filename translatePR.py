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



#Attempting to attach probabilities to guess a word
#Grab output from lstm
output = open("snippet.txt","r")
translation = open('translation29261.txt', 'w')
for line in output:
    string = line.split(' ')
    string = [x for x in string if (x != '' and x != '\n')]
    for word in string:
        if word in ascii2wordDict:
            translation.write(ascii2wordDict[word]+' '),
        else:
            wordCountDict ={}
            for d in word2phDict:
                i=0
                count = 0
                if(len(word2phDict[d])==len(word)):
                    for char in word:
                        #if(char != '\n'): 
                        if ch2phDict[char] == word2phDict[d][i]:
                            count = count+1
                wordCountDict[d] = count
            #print(wordCountDict)
            ''' '''   
            m = 0 #max
            for d in wordCountDict:
                if wordCountDict[d]>m:
                    m=wordCountDict[d]
                    wordChoice = d
            translation.write(wordChoice + ' ')
            ''''''
    translation.write('\n')
translation.close()
