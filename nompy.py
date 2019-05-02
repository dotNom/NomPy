import Feeder
import EventMap
import accessGUI as gui
import settingsGUI as sgui
import filterGUI

def yeartime(event):
    '''
    Takes in an event and puts the date in an int value for comparison
    '''
    time = event.time
    a =  time.tm_year*10E8+time.tm_mon*10E6+time.tm_mday*10E4+time.tm_hour*3600+time.tm_min*60+time.tm_sec
    return int(a)

#Settings gui for setting properties
#All URLS tried/found:
#['http://calendar.utexas.edu/calendar.xml', 
#'http://calendar.mit.edu/calendar.xml', 
#'http://events.umich.edu/day/rss', 
#'http://events.umich.edu/week/rss',
#'https://law.utexas.edu/calendar/feed/rss/',
#'https://music.utexas.edu/events/calendar.xml',
#'https://www.trumba.com/calendars/all-uc-davis-public-events.rss']   

banner = '''
  _   _                 _____       
 | \ | |               |  __ \      
 |  \| | ___  _ __ ___ | |__) |   _ 
 | . ` |/ _ \| '_ ` _ \|  ___/ | | |
 | |\  | (_) | | | | | | |   | |_| |
 |_| \_|\___/|_| |_| |_|_|    \__, |
                               __/ |
                              |___/ 
'''
print(banner, '            by .nom \n')

#Only UT calendars     
defaultALL = ['http://calendar.utexas.edu/calendar.xml','https://law.utexas.edu/calendar/feed/rss/','https://music.utexas.edu/events/calendar.xml', 'https://www.trumba.com/calendars/college-of-communication-event-calendar.rss'] 
defaultFOOD = ['food', 'pizza', 'chinese', 'burgers', 'chicken', 'fries', 'rice', 'refreshments', 'cookies', 'sushi', 'sandwiches', 'coffee', 'dougnuts', 'snacks', 'beer', 'cupcakes', 'brownies', 'tacos', 'breakfast', 'lunch', 'dinner', 'luncheon', 'hotdog', 'beans','chocolate']
a = sgui.setGUI(defaultALL,defaultFOOD)  

print('INITIAL SETTINGS FROM GUI:')
print(a.doCalendar + ' Calendar', a.foodToSearch, a.URLlist, sep = '\n')

foods = a.foodToSearch

#Token gui for plotting map
token = gui.return_token()
mapbox_access_token = token

#calendar
foodEvents = []

#getting all the food events in the url list
for url in a.URLlist:
    print("Working on:", url)
    feeder = Feeder.main(url,foods)
    [foodEvents.append(Es) for Es in feeder.foodEs]
if len(foodEvents) == 0:
    print("didn't find anything :(")
else:
    print('\nOpening webpage')
    #Sorting food events
    Times = list(map(yeartime,foodEvents))
    temp = [ [event,time] for event,time in zip(foodEvents,Times)]
    temp = sorted(temp,key = lambda x: x[1])
    foodEvents = [event[0] for event in temp]
    
    #Do Calendar if desired
    Feeder.doCalendar(foodEvents,a.doCalendar)
    
    #Plot events
    EventMap.plotMap(foodEvents,mapbox_access_token,1)
    
    filteredEvents = filterGUI.return_filter(foodEvents,mapbox_access_token,0)
