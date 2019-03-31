import scrapy
import urllib.request
from PIL import Image
from scrapy.crawler import CrawlerProcess
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

class BrickSetSpider(scrapy.Spider):

	name = 'brick_spider'
	start_urls = ['http://www.me.utexas.edu/faculty/faculty-directory/pryor']

	custom_settings = {'LOG_LEVEL': 'INFO'}

	Images = []
	
	def parse(self, response):		
		self.Images.append(response.xpath('//img').extract_first())
		

process = CrawlerProcess()
process.crawl(BrickSetSpider)
process.start()

hisImage = BrickSetSpider.Images
hisImage = ",".join(hisImage)
hisImage = hisImage.split('"')

print("Url to image is: ",hisImage[1])

urllib.request.urlretrieve(hisImage[1],"DrPryorIMAGE.jpg")

Image.open('DrPryorIMAGE.jpg').show()
