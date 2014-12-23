from TWSS import TWSS
#import urllib2
#from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
from BuildDataSet import getTags


def printTWSS(tags, twss):
    for tag in tags:
        if tag.__class__ == NavigableString:
            phraselist = re.findall(r'\s".+"\s', unicode(tag))
            for phrase in phraselist:
                print phrase + '\n' + twss(phrase)
        else:
            printTWSS(tag, twss)
        print ""


def scrapeTWSS(nPages, txtFile, address, twss):
    for j in range(21, 21+nPages):
        tags = getTags(address, j)
        try:
            printTWSS(tags, twss)
        except:
            pass


if __name__ == '__main__':
    pAddress = 'http://twssstories.com/node?page={0}'
    nPages = 20
    tFile = open('testPositive.txt', 'w')
    twss = TWSS()
    scrapeTWSS(nPages, txtFile=tFile, address=pAddress, twss=twss)
    tFile.close()
