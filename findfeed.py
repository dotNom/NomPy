import requests
from bs4 import BeautifulSoup as bs4


#r = requests.get('https://calendar.utexas.edu/calendar').text
#r = requests.get('https://marcomm.tamu.edu/resources/calendar-feeds.html').text
r = requests.get('https://calendar.mit.edu/calendar').text


rtxt = bs4(r,'lxml')

ctr = 0

for ij in rtxt.findAll("a"):
	
	Attr = ij.attrs
	try:
		Attrhref = Attr['href']
		if Attrhref:
			if Attrhref.find('xml')>=0 or Attrhref.find('rss')>=0:

				if 'title' in Attr:
					print(ctr,':',Attrhref,Attr['title'])
				else:
					print(ctr,':',Attr)
	except KeyError:
		pass

	ctr += 1
