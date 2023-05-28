import scrapy


class PosSpider(scrapy.Spider):
    name = "pos"
    allowed_domains = ["traf.com"]
    start_urls = ["http://traf.com/"]

    def parse(self, response):
        pass
