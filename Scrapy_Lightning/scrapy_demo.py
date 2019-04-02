import scrapy
from scrapy.crawler import CrawlerProcess
import urllib.request
from PIL import Image

class BrickSetSpider(scrapy.Spider):
    name = 'brick_spider'
#    start_urls = ['http://brickset.com/sets/year-1949']
    start_urls = ['http://brickset.com/sets/year-2017']
    image_URL = []
    piece_count = []
    name_count = []
    year_count = []
    price_count = []
    
    def parse(self, response):
        TITLE_SELECTOR = 'title ::text'
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            
            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            COST_SELECTOR = './/dl[dt/text() = "RRP"]/dd[3]/text()'
            COSTalt_SELECTOR = './/dl[dt/text() = "PPP"]/dd[2]/text()' #alternate to capture irregularity

            Cost = brickset.xpath(COST_SELECTOR).extract_first()
            Costalt = brickset.xpath(COSTalt_SELECTOR).extract_first()

            try:
                Cost = Cost.replace(" ",",")
                Cost = Cost.split(",")[0]
                Costalt = Costalt.replace(" ",",")
                Costalt = Costalt.split(",")[0]

                if Costalt[0]=='$': Cost = Costalt #find real cost 
            except: pass

            yield {
                'title': response.css('.no-js').css(TITLE_SELECTOR).extract_first().split()[0],
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
                'cost': Cost,
            }            
            self.year_count.append(response.css('.no-js').css(TITLE_SELECTOR).extract_first().split()[0])
            self.image_URL.append(brickset.css(IMAGE_SELECTOR).extract_first())
            self.piece_count.append(brickset.xpath(PIECES_SELECTOR).extract_first())
            self.name_count.append(brickset.css(NAME_SELECTOR).extract_first())
            self.price_count.append(Cost),

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        else: # If there is not a next page, then go on to the next year
            NEXT_YEAR_SELECTOR = '.col a ::attr(href)'
            next_year = response.css(NEXT_YEAR_SELECTOR).extract()[-1]
            if next_year:
                yield scrapy.Request(
                    response.urljoin(next_year),
                    callback=self.parse
                )
            
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BrickSetSpider)
    process.start() # the script will block here until the crawling is finished
    images = BrickSetSpider.image_URL
    names = BrickSetSpider.name_count
    pieces = BrickSetSpider.piece_count
    year = BrickSetSpider.year_count
    cost = BrickSetSpider.price_count
    
    maxPiece = 0
    maxind = 0
    i = 0
    for piece in pieces:
        if piece is not None:
            if is_int(piece):                 
                if int(piece) > maxPiece:
                    maxPiece = int(piece)
                    maxind = i
        i = i+1
    
    maxName = names[maxind]
    maxImg = images[maxind]
    maxCost = cost[maxind]

    try:
        maxCost = maxCost.replace(" ",",")
        maxCost = maxCost.split(",")[0]
    except: pass

    print()
    print('Biggest Set: {}\n\
    Pieces: {}\n\
    Image URL: {}\n\
    Year: {}\n\
    Cost: {}'\
    .format(maxName,maxPiece,maxImg,year[maxind],maxCost))    

    urllib.request.urlretrieve(maxImg,'Max_Image.png')
    img = Image.open('Max_Image.png')
    img.show()
    
    
    #%% do data science, kinda
    
    # get items with prices in USD
    D = [float(ele.split('$')[1]) if ele is not None and ele.find('$')!=-1 else 0 for ele in cost]
    
    # function to sort junk better
    def findJunk(j):
        if j is not None:
            if j.isnumeric():
                if float(j)>20:
                    return 1
                else:
                    return 0
    # find pieces and stuff
    R = [[y, d/float(s), s] for d, s, y in zip(D, pieces, year) if d!=0 and findJunk(s)]
    
    #calculate price/piece
    years = list(set([float(x[0]) for x in R]))
    YR = []
    yc = []    
    for y in years:
        yc = []
        for x in R:
            if float(x[0]) == y:
               yc.append(x[1]*100)
        YR.append(sum(yc)/len(yc))
        yc = 0
        
    print('Total cost of all sets for all years: ${:.2f}\n\
    Total pieces of all sets for all years {}'\
    .format(sum(D),sum([float(s[2]) for s in R])))
    
    #%% plot data science
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    _=plt.rcParams.update({'font.size': 22})
    _=ax.plot(years,YR)
    _=ax.set(xlabel='year', ylabel='Price/Piece (cents)', title='LEGO prices')