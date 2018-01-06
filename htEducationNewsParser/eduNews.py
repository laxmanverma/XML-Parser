import csv
import urllib2
import xml.etree.ElementTree as ET

def loadRSS():
    url = 'http://www.hindustantimes.com/rss/education/rssfeed.xml'
	
    request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "http://thewebsite.com",
                "Connection": "keep-alive"
        }
    # creating HTTP response object from given url
    resp = urllib2.Request(url, headers = request_headers)
    resp = urllib2.urlopen(resp).read()
    with open('eduNewsfeed.xml', 'wb') as f:
        f.write(resp)

# specifying the fields for csv file
fields = []

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # create empty list for news items
    newsitems = []
    # iterate news items
    for item in root.findall('./channel/item'):
        # empty news dictionary
        news = {}
        for child in item:
            # special checking for namespace object content:media
            if child.tag == '{http://search.yahoo.com/mrss/}content':
                news['media'] = child.attrib['url']
                fields.append('media')
            else:
                news[child.tag] = child.text.encode('utf8')
                fields.append(child.tag)

        newsitems.append(news)

    return newsitems

def savetoCSV(newsitems, filename):
    # specifying the fields for csv
    #fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media']
    with open(filename, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        # writing headers (field names)
        writer.writeheader()
        # writing data rows
        writer.writerows(newsitems)

def main():
    loadRSS()
    newsitems = parseXML('eduNewsfeed.xml')
    savetoCSV(newsitems, 'eduNews.csv')

main()
