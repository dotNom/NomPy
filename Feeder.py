import feedparser
import re
import requests
from bs4 import BeautifulSoup as bs4
import time

def main(url,foods,shouldCalendar):

    start = time.time()
    
    feeder = Feeder(url, foods)
    
    #get full calendar of all events found
    
    #shouldCalendar Do you want calendar of events?:'yes' or 'no'. 
    toStart = 0
    summ = 0
    string = ''
    
    if shouldCalendar.upper()=='YES':
        print("Making Calendar")
        for event in feeder.foodEs:
            #print(event.ICSstr)
#            print(event.summaryICS)
            summ += 1
#            print(summ)
            if toStart == 0: 
                string = addtoICS(event,1)
                toStart += 1
            else:
                string = addtoICS(event,0,string)
                                  
        if string:
            writetoICS(string,'CollatedICS.ics')
        print('Calendar saved as "CollatedICS.ics"\ndone')
    end = time.time()
    
    pie='''
            )
                 (
              )
         __..---..__
     ,-='  /  |  \  `=-.
    :--..___________..--;
     \.,_____________,./
     '''
    print(pie)
    print('\nOpening webpage')
    print('runtime:',end-start,'s')
    return feeder

def validlink(link,debugMode=1):
    '''
    Function takes in a single xml or rss link and see if it exists
    '''
    
    isValid = False
    
    try:
        requests.head(link)
        isValid = True        
        if debugMode == 1:
            print('ValidURL')

    except:
         if debugMode == 1:
            print('Exception raised: InvalidURL')
            
    return isValid
    
def findRSSonPAGE(linklist,*string,debugMode=1):
    
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
                        for entr in string:
                            if Attrhref.find(entr)>=0:
                            
#                                if debugMode == 1:
#                                    if 'title' in Attr:
#                                        print(ctr,':',Attrhref,Attr['title'])
#                                    else:
#                                        print(ctr,':',Attr)
                                        
                                isRss[ct] = True
                                if Attrhref not in RssLink_s[ct]:
                                    RssLink_s[ct].append(Attrhref)
                            
                except KeyError:
                    if debugMode == 1:
                        print('KeyError because No href key')
            
                ctr += 1

        except:
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
        if event.timeend: fillme.append(event.timeend+'\n')
        if event.timestart: fillme.append(event.timestart+'\n')           
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
    
class ICStoRSStime:

    def __init__(self,ICS):
        ICS = ICS.split(':')[-1]
        self.tm_year = int(ICS[0:4])
        self.tm_mon = int(ICS[4:6])
        self.tm_mday = int(ICS[6:8])
        
        if 'T' in ICS: #not Allday
            self.tm_hour = int(ICS[9:11])
            self.tm_min = int(ICS[11:13])
            self.tm_sec = int(ICS[13:15])
        else: #Allday event
            self.tm_hour = 0
            self.tm_min = 0
            self.tm_sec = 0
            
    def __str__(self):
        out = '('
        for attr, value in self.__dict__.items():
            out += ' ' + attr + ' = ' + str(value) + ','
        out = out.strip(',')
        out += ' )'
        return out
    
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
        
    def __init__(self, event, foods, track, trumba_ical = None):
        '''
        basic init
        make smarter/more robust later
        '''

        self.food = re.findall(r"(?=("+'|'.join(foods)+r"))", event.summary)
        if 'free' in event.summary.lower(): self.free = True 
        else: self.free = False
        
        names = ['title', 'summary', 'location', 'location', 'time', 'link', '_id']
        icsnames = ['timestart', 'timeend', 'timestamp', 'locwithBUI', 'descriptionICS', 'summaryICS']
        [setattr(self, name, None) for name in names + icsnames]

        self.track = track[0]
        self.ext = track[1]
        self.ICSyes = track[2]
        
        if 'title' in event.keys(): self.title = event.title
        if 'summary' in event.keys(): self.summary = event.summary
        if 'published_parsed' in event.keys(): self.time = event.published_parsed #not sure if we should use published_parsed or updated_parsed
        if 'link' in event.keys(): self.link = event.link
        
        #specific hack for UMich and UTlaw
        if 'id' in event.keys(): self._id = event.id
        
        #specific hack for trumba
        self._trumba_ical = trumba_ical
        if self._trumba_ical: self._id = event.id.split('/')[-1]
        
        self._make_geo(event)
        
        if self._trumba_ical:
            self.ICSyes = 1
            self._getICSprops()
            self.time = ICStoRSStime(self.timestart)
        elif self.link:
            if self.track==0:
                print('Checking for ics in ', self.link,'\n')
                ynICS, ICSlink = findRSSonPAGE(self.link,'.ics','/ical','/ics',debugMode=1)
                if ynICS:
#                    print('In ',self.link,'  find ics extra')
                    if 'umich' in self._id:
                        self.ICSyes = 1
                    elif self.link.split(':')[1] in ICSlink[0].split(':')[1]:
                        self.ext = ICSlink[0].split(':')[1].split(self.link.split(':')[1])[1]
                        self.ICSyes = 1
#                        print('ics extra: ', self.ext,'\n')
                               
            self._getICSprops()
#            print('Done ics')
     
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
        
        def cleanline(toRet,extract):
            
            Allatr = ['DTSTART','DTEND','DTSTAMP','LOCATION','DESCRIPTION','SUMMARY'] #all known attributes to search for
            
            #Get rid of redundancies, basically make cleaner expressions:
            for string in Allatr:
                if string != extract:
                    toRet = toRet.split(string)[0]
             
            return toRet
        
        toRet = None

        if type(a)==str:
            a = a.split('\n')
            found = None

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
                            toRet = cleanline(toRet,extract)
                            return toRet
                        else:
                            toRet += itm.strip()
                    else:
                        toRet += itm.strip()

        if toRet: toRet = cleanline(toRet,extract)
                        
        return toRet
        
    def _formatTIME(self,intime):
    
        '''format python timestruct into form to compare with ics time'''
    
        intime=str(intime)
        if len(intime)==1: intime='0'+intime
        return intime
    
    def _calTIME(self,intime):
        '''
        returns time in right format for display in calendar
        '''
        timesday = self._formatTIME(intime.tm_year)+self._formatTIME(intime.tm_mon)+self._formatTIME(intime.tm_mday)
        timesday += 'T' + self._formatTIME(intime.tm_hour)+self._formatTIME(intime.tm_min)+self._formatTIME(intime.tm_sec)
        return timesday
        
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
        #specific hack for UT law
        elif 'law.utexas' in self._id:
            url = link + 'ics/'
        else:
            url = link + '.ics'
            
        if self._trumba_ical:
            myICS = [ics for ics in self._trumba_ical.split('BEGIN') if self._id in ics]
            
        else:
            myICS = requests.get(url).text #retrieve ics and save as string in myICS
            # UT is rate limiting us and pausing the ics downloads
            time.sleep(.5)
       
            #clean up the stuff in the ics file
            myICS = myICS.split('BEGIN')
        if self.time:
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
        else:
            myICS = myICS[0]
                
        if type(myICS)==list:
            myICS = ''#.join(myICS)

        
        return myICS
    
    def _getICSprops(self):
        
        '''
            takes in an self eg: test.foodEs[0] and gets the time (start and end) as well as the building and location
            from the ics file
        '''
        
        if self.ICSyes == 1:
            self.ICSstr = self._get_ics(self.link,self.time)
            self.timestart = self._extractICS(self.ICSstr,'DTSTART')
            self.timeend = self._extractICS(self.ICSstr,'DTEND')
            self.timestamp = self._extractICS(self.ICSstr,'DTSTAMP')
            self.locwithBUI = self._extractICS(self.ICSstr,'LOCATION') #location with building number
            self.descriptionICS = self._extractICS(self.ICSstr,'DESCRIPTION') #description of event from ics
            self.summaryICS = self._extractICS(self.ICSstr,'SUMMARY')
        else:
            if self.time: self.timestart = 'DTSTART:' + self._calTIME(self.time)
            self.timestamp = 'DTSTAMP:' + self._calTIME(time.gmtime())
            self.summaryICS = 'SUMMARY:' + self.title
            self.descriptionICS = 'DESCRIPTION:' + ''.join(''.join(self.summary.split('<a')[0].split('</p>')).split('<p>'))
            
class Feeder:
    ''' Interact with RSS feed '''
    
    def __init__(self, url, foods):
        self.url = url
        self.foods = foods
        self.feed = feedparser.parse(url)
        if 'etag' in self.feed.keys(): self.etag = self.feed.etag
        self.track = [0,'',0]
        
        self.trumba_ical = None
        if 'trumba' in url:
            self.trumba_ical = requests.get('.'.join(url.split('.')[:-1]) + '.ics').text
        
        self.make_foodEs()
        
    def update(self,url):
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
        self.foodEs = []
        spinner = spinning_cursor()

        for event in self.feed.entries:
            try:
                if re.findall(r"(?=("+'|'.join(self.foods)+r"))", event.summary):
                    foodtile = foodE(event, self.foods, self.track, trumba_ical=self.trumba_ical)
                    self.foodEs.append(foodtile)
                    self.track[0] += 1
                    self.track[1] = foodtile.ext
                    self.track[2] = foodtile.ICSyes

                    print('\r' + next(spinner)+' Got '+str(self.track[0])+' ics events'.format(self.track[0]),end='')
            except:
                print('bad event')
        print('\n')
                
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

'''
if __name__ == '__main__':
    feeder = main('http://events.umich.edu/week/rss',['food'],'YES')
    feeder = main('http://calendar.utexas.edu/calendar.xml',['food'],'YES')
    feeder = main('https://www.trumba.com/calendars/all-uc-davis-public-events.rss',['food'],'YES')
foods = ['food']
#    url = 'calendar.xml'
url = 'http://calendar.utexas.edu/calendar.xml'
#    url = 'http://calendar.mit.edu/calendar.xml'
#url = 'http://events.umich.edu/week/rss'
#url = 'https://law.utexas.edu/calendar/feed/rss/'
# michigan has quite different format and no geo, but it doesn't break
print(url)
feeder = main(url,foods,'yes')
'''
