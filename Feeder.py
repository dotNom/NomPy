import feedparser
import re
import urllib.request
import requests
from bs4 import BeautifulSoup as bs4

#add function that checks for if link provided has rss feed and returns the link to the feed

def extractICS(a,extract):
    
    '''
    extracts certain lines from the ics file. extract must be a keyword string examples:
        DTEND for end time
        DTSTART for start time
        LOCATION for building name and room number
    '''
    
    a = a.split('\n')
    for itm in a:
        if itm.find(extract)>=0:
            return itm
        
def get_ics(link):
    
    '''
    get ics file from the link in the event
        ics on the link has all the times, so parse the ics file so that
        you only get the time event that matches the extracted time in the event
    '''
    
    #need to fix this so that it only get the time that matters
    url = link
    urllist = [url,'.ics']
    url = ''.join(urllist)
    urllib.request.urlretrieve(url,'temp.ics')
    
    #clean up the stuff in the ics file
    with open('temp.ics', encoding = "utf8", mode = 'r') as myfile:
        myICS = myfile.read()
    
    myICS = myICS.split('BEGIN')
    myICS = 'BEGIN'.join(myICS[0:3])
    
    return myICS

def getICSprops(event):
    
    '''
        takes in an event eg: test.foodEs[0] and gets the time (start and end) as well as the building and location
        from the ics file
    '''
    
    ICSstr = get_ics(event.link)
    event.timestart = extractICS(ICSstr,'DTSTART')
    event.timeend = extractICS(ICSstr,'DTEND')
    event.timestamp = extractICS(ICSstr,'DTSTAMP')
    event.locwithBUI = extractICS(ICSstr,'LOCATION') #location with building number
    event.category = extractICS(ICSstr,'CATEGORIES') #category of event
    event.summary = extractICS(ICSstr,'SUMMARY')

def addtoICS(event,start,oldstring = ''):
    
    '''
        Create ICS string for file in the format to open up in calendar
    '''
    #add name -> need to parse out the description so that it only gets valid stuff
    #name is summart
    fillme = []
    
    if start == 1 and len(oldstring)==0: #yes starting a new calendar
        fillme.append('BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nPRODID:iCalendar-Ruby\n')
        
    fillme.append('BEGIN:VEVENT\n')
    
    if event.category: fillme.append(event.category+'\n')
    if event.description: fillme.append('DESCRIPTION:'+event.description+'\n')
    if event.timeend: fillme.append(event.timeend+'\n')
    if event.timestart: fillme.append(event.timestart+'\n')
    if event.timestamp: fillme.append(event.timestamp+'\n')
    if event.locwithBUI: fillme.append(event.locwithBUI+'\n')
    if event.summary: fillme.append(event.summary+'\n')
    
    fillme.append('END:VEVENT\n')
    
    newstring = ''.join(fillme)
    
    return oldstring+newstring

def writetoICS(string,filename='Food_Calendar.ics'):
    
    '''
        Write string to fileName
    '''
    
    with open(filename, encoding = "utf8", mode = 'w') as myfile:
        myfile.write(string)    
    
    
class foodE:
    ''' Food event generated from calendar feed'''

    def __init__(self, event, foods):
        '''
        basic init
        make smarter/more robust later
        
        
        '''
        self.food = re.findall(r"(?=("+'|'.join(foods)+r"))", event.summary)
        names = ['title', 'description', 'location', 'location', 'time', 'link']        
        [setattr(self, name, None) for name in names]

#        elements = ['title', 'summary', 'geo_lat', 'geo_long', 'updated_parsed', 'link']
#        [self._ccreate(event, element, name) for name, element in zip(names,elements)]
        
        if 'title' in event.keys(): self.title = event.title
        if 'summary' in event.keys(): self.summary = event.summary
        if 'updated_parsed' in event.keys(): self.time = event.updated_parsed
        if 'link' in event.keys(): self.link = event.link
        
        self.make_location(event)
        
    #maybe better way to do init
    def make_location(self, event):
        if hasattr(event, 'geo_lat'):
            self.geo = (float(event.geo_lat), float(event.geo_long))
        
    def _ccreate(self, event, element, name):
        if element in event.keys():
            value = event[element]
            if hasattr(self, name):
                value = (value, getattr(self, name))
            setattr(self, name, value)
                
class Feeder:
    ''' Interact with RSS feed '''
    
    def __init__(self, url, foods):
        self.url = url
        self.foods = foods
        self.feed = feedparser.parse(url)
        if 'etag' in self.feed.keys(): self.etag = self.feed.etag
        self.make_foodEs()
        
    def update(self):
        if hasattr(self, 'etag'):
            feed_temp = feedparser.parse(self.url, self.etag)
            if feed_temp.status == 304:
                print('no updates')
            else:
                self.feed = feed_temp
                self.make_foodEs()
        else:
            print('no etag')
            self.feed = feedparser.parse(url)
            if 'etag' in self.feed.keys(): self.etag = self.feed.etag
            self.make_foodEs()
                
    def make_foodEs(self):
        self.foodEs = [foodE(event, self.foods) for event in self.feed.entries 
                       if re.findall(r"(?=("+'|'.join(self.foods)+r"))", event.description)]

if __name__ == '__main__':
                
    foods = ['food', 'pizza', 'chinese', 'burgers', 'chicken', 'fries', 'rice', 'refreshments', 'cookies', 'sushi', 'sandwiches', 'coffee', 'dougnuts', 'snacks', 'beer', 'cupcakes', 'brownies', 'tacos']
    #fix regex
    #tiff's tiffs Tiffs
    
    #local calendar
#    url = 'calendar.xml'
#    url = 'http://calendar.utexas.edu/calendar.xml'
#    url = 'http://calendar.mit.edu/calendar.xml'
    url = 'http://events.umich.edu/day/rss'
    
    feeder = Feeder(url, foods)
