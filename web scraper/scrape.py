from lxml import html
import requests
from random import shuffle
finalList = []
source = [(22,"general"), (41,"dirty"), (7,"nerdy")]
for sauce in source:
    for i in range(sauce[0]):
        page = requests.get('http://www.funlimericks.com/'+sauce[1]+'-limericks.php?page='+str(i))
        tree = html.fromstring(page.content)
        limericks = tree.xpath('//blockquote[@class="style3"]//span/text()')
        pageList = []
        comb = ""
        for x in range(int(len(limericks)/5)):
            comb = limericks[5*x] + '\n' + limericks[5*x + 1] + '\n' + limericks[5*x + 2] + '\n' + limericks[5*x + 3] + '\n' + limericks[5*x + 4]
            pageList.append(comb)
            comb = ""
        finalList += pageList
shuffle(finalList)
#print(str(len(finalList)) + " Limericks scraped from funlimericks.com")
for z in range(len(finalList)):
	print(finalList[z]+"\n\n")
