import feedparser
import re
import requests
from bs4 import BeautifulSoup as bs4
import time

def checkforRSS(linklist,debugMode=1):
    
    '''
    Function takes in a single link or a set of links to find if there is an rss feed
    in the provided page, and it returns 2 arguments:
        True or False if there is/isn't an rss feed in the link
        a list containing links to all rss feeds found (empty if no feed)
    If a list or tuple is given, then it returns the above in two different lists
    One of Trues and Falses depending on if an rss feed was found on the page
    The other of lists containing sublists which hold the links to these feeds 
    '''
    
    if type(linklist) != list and type(linklist) != tuple:
        temp = [linklist]
        linklist = temp.copy()
        
    isRss = []
    RssLink_s = []
    
    ct = 0
    
    for link in linklist:
        RssLink_s.append([])
        isRss.append(False)
        try:
            r = requests.get(link).text
        
            rtxt = bs4(r,'lxml')
            
            ctr = 0
            
            for ij in rtxt.findAll("a"):
            	
                Attr = ij.attrs
                try:
                    Attrhref = Attr['href']
                    if Attrhref:
                        if Attrhref.find('xml')>=0 or Attrhref.find('rss')>=0:
                        
                            if debugMode == 1:
                                if 'title' in Attr:
                                    print(ctr,':',Attrhref,Attr['title'])
                                else:
                                    print(ctr,':',Attr)
                                    
                            isRss[ct] = True
                            if Attrhref not in RssLink_s[ct]:
                                RssLink_s[ct].append(Attrhref)
                            
                except KeyError:
                    if debugMode == 1:
                        print('KeyError because No href key')
            
                ctr += 1
        
        except requests.exceptions.InvalidURL: 
            if debugMode == 1:
                print('Exception raised: InvalidURL')
                
        ct += 1
    
    if len(isRss)==1:
        return isRss[0], RssLink_s[0]
    else:
        return isRss, RssLink_s

def addtoICS(event,start,oldstring = ''):
    
    '''
        Create ICS string for file in the format to open up in calendar
    '''
    
    #name is summart
    fillme = []
    
    if start == 1 and len(oldstring)==0: #yes starting a new calendar
        fillme.append('BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nPRODID:iCalendar-Ruby\n')
    
    if event.summaryICS:
        fillme.append('BEGIN:VEVENT\n')
        
        if event.descriptionICS: fillme.append(event.descriptionICS+'\n')
        if event.timeend:
            if event.timeend in event.timestamp:
                event.timestamp = event.timestamp.split(event.timeend)[0]
            if event.timeend in event.timestart:
                event.timestart = event.timestart.split(event.timeend)[0]
            fillme.append(event.timeend+'\n')
        if event.timestart: 
            if event.timestart in event.timestamp:
                event.timestamp = event.timestamp.split(event.timestart)[0]
            fillme.append(event.timestart+'\n')
        if event.timestamp: fillme.append(event.timestamp+'\n')
        if event.locwithBUI: fillme.append(event.locwithBUI+'\n')
        if event.summaryICS: fillme.append(event.summaryICS+'\n')
        
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
    ''' Food event generated from calendar feed
        Object Properties
        
        title: title string
        summary: messy summary string that may include some html stuff
        time: python time struct in UTC
        link: link string to calendar event page
        geo: tuple(lat,long) of floats
        free: Boolean indicator that the text 'free' is somewhere in there
        
        Other ICS attribs, not sure yet
        
        '''
        
    def __init__(self, event, foods):
        '''
        basic init
        make smarter/more robust later
        '''

        self.food = re.findall(r"(?=("+'|'.join(foods)+r"))", event.summary)
        if re.findall(r"(?=("+'|'.join('free')+r"))", event.summary): self.free = True 
        
        names = ['title', 'summary', 'location', 'location', 'time', 'link', '_id']
        icsnames = ['timestart', 'timeend', 'timestamp', 'locwithBUI', 'descriptionICS', 'summaryICS']
        [setattr(self, name, None) for name in names + icsnames]

#        elements = ['title', 'summary', 'geo_lat', 'geo_long', 'updated_parsed', 'link']
#        [self._ccreate(event, element, name) for name, element in zip(names,elements)]
        
        if 'title' in event.keys(): self.title = event.title
        if 'summary' in event.keys(): self.summary = event.summary
        if 'published_parsed' in event.keys(): self.time = event.published_parsed #not sure if we should use published_parsed or updated_parsed
        if 'link' in event.keys(): self.link = event.link
        
        #specific hack for UMich
        if 'id' in event.keys(): self._id = event.id
        
        self._make_geo(event)
        
        if self.link:
            self._getICSprops()
            print('got ics')
        
    #maybe better way to do init
    def _make_geo(self, event):
        if hasattr(event, 'geo_lat'):
            self.geo = (float(event.geo_lat), float(event.geo_long))
        
    def _ccreate(self, event, element, name):
        if element in event.keys():
            value = event[element]
            if hasattr(self, name):
                value = (value, getattr(self, name))
            setattr(self, name, value)
            
    def _extractICS(self, a, extract):
        
        '''
        extracts certain lines from the ics file. extract must be a keyword string examples:
            DTEND for end time
            DTSTART for start time
            LOCATION for building name and room number
        '''

        try:
            a = a.split('\n')
            found = None
            toRet = None
            
            for itm in a:      
                if itm.find(extract)>=0:
                    toRet = itm.strip()
                    found = a.index(itm)
                    break
            
            if found != None:
                for itm in a[found+1:]:
                    itmNew = itm.split(':')
                    if len(itmNew)>1:
                        if itmNew[0].isupper():
                            return toRet
                        else:
                            toRet += itm.strip()
                    else:
                        toRet += itm.strip()
            
            return toRet
        except:
            return None
        
    def _formatTIME(self,intime):
    
        '''format python timestruct into form to compare with ics time'''
    
        intime=str(intime)
        if len(intime)==1: intime='0'+intime
        return intime
    
    def _get_ics(self, link, intime):
        
        '''
        get ics file from the link in the event
            ics on the link has all the times, so parse the ics file so that
            you only get the time events that are in the future
        find ics event that is closest
        '''
        
        #specific hack for UMich
        if 'umich' in self._id:
            url = link + '-' + self._id.split('@')[0].split('-')[1] + '/feed/ical'
        else:
            url = link + '.ics'
        
        myICS = requests.get(url).text #retrieve ics and save as string in myICS
       
        #clean up the stuff in the ics file
        myICS = myICS.split('BEGIN')
    
        for entry in myICS:
            #try:
            start = self._extractICS(entry,'DTSTART')
            if start:
                start = start.split(':')
                del(start[0])
                start = start[0]
                reftime=self._formatTIME(intime.tm_year)+self._formatTIME(intime.tm_mon)+self._formatTIME(intime.tm_mday)
                if int(reftime)<=int(start[0:8]):
                    myICS = entry
                    break
                
        if type(myICS)==list:
            myICS = ''#.join(myICS)
            #except:
                #pass
        # UT is rate limiting us and pausing the ics downloads
        time.sleep(.5)
        
        return myICS
    
    def _getICSprops(self):
        
        '''
            takes in an self eg: test.foodEs[0] and gets the time (start and end) as well as the building and location
            from the ics file
        '''
        self.ICSstr = self._get_ics(self.link,self.time)
        self.timestart = self._extractICS(self.ICSstr,'DTSTART')
        self.timeend = self._extractICS(self.ICSstr,'DTEND')
        self.timestamp = self._extractICS(self.ICSstr,'DTSTAMP')
        self.locwithBUI = self._extractICS(self.ICSstr,'LOCATION') #location with building number
        self.descriptionICS = self._extractICS(self.ICSstr,'DESCRIPTION') #description of event from ics
        self.summaryICS = self._extractICS(self.ICSstr,'SUMMARY')

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
    
    start = time.time()
    
#    foods = ['food', 'pizza', 'chinese', 'burgers', 'chicken', 'fries', 'rice', 'refreshments', 'cookies', 'sushi', 'sandwiches', 'coffee', 'dougnuts', 'snacks', 'beer', 'cupcakes', 'brownies', 'tacos']
    foods = ['food']
    #need to fix regex
    #tiff's tiffs Tiffs
    
    #local calendar
#    url = 'calendar.xml'
#    url = 'http://calendar.utexas.edu/calendar.xml'
#    url = 'http://calendar.mit.edu/calendar.xml'
#    url = 'http://events.umich.edu/day/rss'
    url = 'http://events.umich.edu/week/rss'
#    url = 'michigan.xml'
    # michigan has quite different format and no geo, but it doesn't break
    
    feeder = Feeder(url, foods)
    
    #get full calendar of all events found
    
    shouldCalendar = 'yes' #Do you want calendar of events?:'yes' or 'no'. 
    toStart = 0
    summ = 0
    
    if shouldCalendar.upper()=='YES':
        for event in feeder.foodEs:
            #print(event.ICSstr)
            print(event.summaryICS)
            summ += 1
            print(summ)
            if toStart == 0: 
                string = addtoICS(event,1)
                toStart += 1
            else:
                string = addtoICS(event,0,string)
                                  
        
        writetoICS(string,'CollatedICS.ics')
        
    end = time.time()
    
    print('runtime:',end-start,'s')