import feedparser
import re

class foodE:
    ''' Food event generated from calendar feed'''

    def __init__(self, event, foods):
        '''
        basic init
        make smarter/more robust later
        '''
        self.food = re.findall(r"(?=("+'|'.join(foods)+r"))", event.summary)
        
        elements = ['title', 'summary', 'geo_long', 'geo_lat', 'updated_parsed', 'link']
        names = ['title', 'description', 'location', 'location', 'time', 'link']
        
        [self.ccreate(event, element, name) for name, element in zip(names,elements)]
        
        self.make_location(event)
        
    #maybe better way to do init
    def make_location(self, event):
        if hasattr(event, 'geo_lat'):
            self.location = (float(event.geo_long), float(event.geo_lat))
        
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
        if 'etag' in self.feed.keys(): self.etag = self.feed.etag
        self.make_foodEs()
        
    def update(self):
        if hasattr(self, 'etag'):
            feed_temp = feedparser.parse(self.url, self.etag)
            if feed_temp.status == 304:
                print('no updates')
            else:
                self.feed = feed_temp
                self.make_foodEs
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
    #tiff's tiffs Tiffs
    
    #local calendar
#    url = 'calendar.xml'
    url = 'http://calendar.utexas.edu/calendar.xml'
#    url = 'http://calendar.mit.edu/calendar.xml'
    
    test = Feeder(url, foods)
