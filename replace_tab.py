import codecs
inf = open('cmuDict_seq2seq.txt', 'r')
toWrite = open('cmuFormatted.txt', 'w')
for line in inf:
    split_line = line.split()
    #new_str = split_line[0] + '\t' + ''.join(split_line[1:])
    new_str = " ".join(split_line[1:]) + '\t' + split_line[0]
    toWrite.write(new_str+'\n')
    #print(new_str)
inf.close()
toWrite.close()