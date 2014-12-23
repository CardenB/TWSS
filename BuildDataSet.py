from DataScraper import DataScraper
import urllib2
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re


def scrape(address, numPages, fName, regex):
    scraper = DataScraper(fName, address=address)
    scraper.regex = r'Today,.+'
    scraper.fetchData(numPages=numPages)
    scraper.closeFile()


def writePhrase(txtFile, phrase):
    try:
        txtFile.write(phrase + " ")
        print phrase
    except UnicodeEncodeError:
        pass


def getTags(address, pageNum):
    url = address.format(pageNum)
    print "\nScraping page {num} on {addr}..."\
        .format(num=pageNum, addr=url)
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    tags = soup.findAll('p')
    return tags


def printTWSS(tags, txtFile):
    for tag in tags:
        if tag.__class__ == NavigableString:
            phraselist = re.findall(r'\s".+"\s', unicode(tag))
            for phrase in phraselist:
                writePhrase(txtFile, phrase)
                txtFile.write(phrase+'\n\n')
        else:
            printTWSS(tag, txtFile)
        print ""


def scrapeTWSS(nPages, txtFile, address):
    for j in range(nPages):
        tags = getTags(address, j)
        printTWSS(tags, txtFile)


def scrapeFML(nPages, txtFile, address):
    for j in range(nPages):
        tags = getTags(address, j)
        for tag in tags:
            phraseTags = tag.findAll('a')
            for pTag in phraseTags:
                if 'class' in pTag.attrs.keys()\
                        and pTag['class'][0] == "fmllink":
                    phrase = pTag.get_text()
                    if 'FML' in phrase:
                        txtFile.write('\n\n')
                    else:
                        writePhrase(txtFile, phrase)


def scrapeTFLN(nPages, txtFile, address):
    for j in range(nPages):
        tags = getTags(address, j)
        for tag in tags:
            pTags = tag.findAll('a')
            for pTag in pTags:
                if 'href' in pTag.attrs.keys()\
                        and 'Text-Replies' in pTag['href']:
                    phrase = pTag.get_text()
                    writePhrase(txtFile, phrase)
            txtFile.write('\n\n')


if __name__ == '__main__':
    pAddress = 'http://twssstories.com/node?page={0}'
    nPages = 20
    tFile = open('positive.txt', 'w')
    scrapeTWSS(nPages, txtFile=tFile, address=pAddress)
    tFile.close()

    tFile = open('negative.txt', 'w')
    nAddress = 'http://www.fmylife.com/?page={0}'
    scrapeFML(nPages, txtFile=tFile, address=nAddress)

    nAddress = 'http://textsfromlastnight.com/texts/page:{0}'
    scrapeTFLN(nPages, txtFile=tFile, address=nAddress)
    tFile.close()
