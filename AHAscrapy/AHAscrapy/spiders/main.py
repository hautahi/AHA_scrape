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
        item['content'] = soup.get_text(separator=" ", strip=True)
        return item
