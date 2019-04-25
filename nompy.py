import Feeder
import EventMap
import accessGUI as gui

token = gui.return_token()
mapbox_access_token = token

#foods = ['food', 'pizza', 'chinese', 'burgers', 'chicken', 'fries', 'rice', 'refreshments', 'cookies', 'sushi', 'sandwiches', 'coffee', 'dougnuts', 'snacks', 'beer', 'cupcakes', 'brownies', 'tacos']
foods = ['food']
#need to fix regex
#tiff's tiffs Tiffs

#local calendar
#    url = 'calendar.xml'
url = 'http://calendar.utexas.edu/calendar.xml'
#    url = 'http://calendar.mit.edu/calendar.xml'
#    url = 'http://events.umich.edu/day/rss'
# michigan has quite different format and no geo, but it doesn't break

feeder = Feeder.main(url,foods)
#    feeder = Feeder(url, foods)
foodEvents = feeder.foodEs

EventMap.plotMap(foodEvents,mapbox_access_token)