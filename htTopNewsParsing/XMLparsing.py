import csv
import requests
import xml.etree.ElementTree as ET

def loadRSS():
    url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'
    # creating HTTP response object from given url
    resp = requests.get(url)
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)

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
                news[child.tag] = child.text#.encode('utf8')
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
    newsitems = parseXML('topnewsfeed.xml')
    savetoCSV(newsitems, 'topnews.csv')

if __name__ == "__main__":
    main()
