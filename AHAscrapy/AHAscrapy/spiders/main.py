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
    #allowed_domains = ['hautahi.com']
    #start_urls = ['http://hautahi.com']

    def __init__(self,al=None,*args,**kwargs):
        super(MySpider,self).__init__(*args,**kwargs)
        
        start_urls = ['http://hautahi.com']
        if 'url' in kwargs:
            self.start_urls = [kwargs.get('url')]
        else:
            self.start_urls = stast_urls

        self.allowed_domains = [al]

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True), )

    def parse_url(self, response):
        item = MyItem()
        item['url'] = response.url
        soup = BeautifulSoup(response.body, "lxml")
        item['content'] = soup.get_text(separator=" ", strip=True)
        return item
