# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET
 
def loadRSS():
    # url of rss feed
    url = 'http://synd.cricbuzz.com/j2me/1.0/livematches.xml'
    # creating HTTP response object from given url
    resp = requests.get(url)
    # saving the xml file
    with open('liveMatch.xml', 'wb') as f:
        f.write(resp.content)
"""
The wb indicates that the file is opened for writing in binary mode.
On Unix systems (Linux, Mac OS X, etc.), binary mode does nothing - they
treat text files the same way that any other files are treated. 
On Windows, however, text files are written with slightly modified line 
endings. This causes a serious problem when dealing with actual 
binary files, like exe or jpg files. Therefore, when opening files which 
are not supposed to be text, even in Unix, you should use wb or rb. 
Use plain w or r only for text files.
"""
# specifying the fields for csv file
fields = []
def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
    # create empty list for news items
    newsitems = []
    # iterate news items
    for item in root.findall('./match'):
        # empty news dictionary
        news = {}
        # iterate child elements of item
        for child in item:
            fields.append(child.tag)
            news[child.tag] = child.attrib
            #news[child.tag] = child.text
        # append news dictionary to news items list
        newsitems.append(news)
 
    # return news items list
    return newsitems
 
def savetoCSV(liveupdates, filename):
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        # writing headers (field names)
        writer.writeheader()
        # writing data rows
        writer.writerows(liveupdates)
 
def main():
    # load rss from web to update existing xml file
    loadRSS()
    # parse xml file
    liveupdates = parseXML('liveMatch.xml')
    # store news items in a csv file
    savetoCSV(liveupdates, 'update.csv')
 
if __name__ == "__main__":
    # calling main function
    main()
