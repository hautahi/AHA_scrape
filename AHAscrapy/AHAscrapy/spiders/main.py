from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.linkextractor import LinkExtractor
from bs4 import BeautifulSoup
import csv
from AHAscrapy import settings

class MyItem(Item):
    content=Field()
    url= Field()

class MySpider(CrawlSpider):

    name = 'AHAscrape'

    def __init__(self,al=None,allow_subdom=None,*args,**kwargs):
        super(MySpider,self).__init__(*args,**kwargs)
        
        # Declare the start url and allowed domains from inputs
        self.start_urls = [kwargs.get('url')]
        self.allowed_domains = [al]
        
        # Declare rules which include limiting search to appropriate subdomains
        MySpider.rules = (Rule(LinkExtractor(allow=(allow_subdom)), callback='parse_url', follow=True), )
        super(MySpider,self)._compile_rules()

    def parse_url(self, response):
        item = MyItem()
        item['url'] = response.url
        soup = BeautifulSoup(response.body, "lxml")

		# kill all script and style elements
        for script in soup(["script", "style"]):
				script.extract()    # rip it out

        text = soup.get_text(separator=" ", strip=True)
        lines = (line.strip() for line in text.splitlines())
		
		# break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        #item['content'] = soup.get_text(separator=" ", strip=True)
        item['content'] = text
        return item
