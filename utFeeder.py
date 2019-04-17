import feedparser
import re

class foodE:
    ''' Food event generated from calendar feed'''

    def __init__(self, event, foods):
        '''
        basic init
        make smarter/more robust later
        '''
        self.food = re.findall(r"(?=("+'|'.join(foods)+r"))", event.description)
        
        elements = ['title', 'geo_lat', 'geo_long', 'updated_parsed']
        names = ['title', 'location', 'location', 'time']
        
        [self.ccreate(event, element, name) for name, element in zip(names,elements)]
        
    def ccreate(self, event, element, name):
        if element in event.keys():
            value = event[element]
            if hasattr(self, name):
                value = (value, getattr(self, name))
            setattr(self, name, value)        
            
    def _get_ics(self):
        print('idk')
        
class Feeder:
    ''' Interact with RSS feed '''
    
    def __init__(self, url, foods):
        self.url = url
        self.foods = foods
        self.feed = feedparser.parse(url)
        if 'etag' in self.feed.keys():
            self.etag = self.feed.etag
        self.foodEs = [foodE(event, self.foods) for event in self.feed.entries 
             if re.findall(r"(?=("+'|'.join(self.foods)+r"))", event.description)]
        
    def update(self):
        feed_temp = feedparser.parse(self.url, self.etag)
        if feed_temp.status == 304:
            print('no updates')
        else:
            self.feed = feed_temp

if __name__ == '__main__':
                
    foods = ['food', 'pizza']
    
    #local calendar
    url = 'calendar.xml'
#    url = 'http://calendar.utexas.edu/calendar.xml'
    
    test = Feeder(url, foods)