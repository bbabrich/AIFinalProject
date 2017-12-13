import codecs
inf = open('cmu_shuf.txt', 'r')
for line in inf:
    split_line = line.split()
    #new_str = split_line[0] + '\t' + ''.join(split_line[1:])
    new_str = "".join(split_line[1:]) + "\t" + split_line[0]
    print(new_str)
