import scrapy
from scrapy_playwright.page import PageMethod

class PosSpider(scrapy.Spider):
    name = "trafigura"
    allowed_domains = ["trafigura.com"]
    start_urls = ["https://careers.trafigura.com/TrafiguraCareerSite/search"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],
                             meta=dict(playwright=True,
                                       playwright_page_methods=[PageMethod('wait_for_selector', 'section#results'),
                                                                PageMethod("evaluate", """
                            const interval_id = setInterval(function() {
                             const button = document.querySelector('#results > div.py-3.ng-star-inserted > button');
                             if (button) {
                                 button.scrollIntoView();
                                 button.click();
                             } else {
                                 clearInterval(interval_id)
                             }
                             }, 1000)"""),
                                                                PageMethod('wait_for_selector',
                                                                           '#results > div.py-3.ng-star-inserted > button',
                                                                           state='detached')]))

    async def parse(self, response):
        for job in response.css('section#results div[class="list-group"] div[role="listitem"]'):
            yield {
                "title": job.css('a::text').get(),
                'location': job.css('div[aria-describedby="header-location"]::text').get(),
                'category': job.css('div[aria-describedby="header-category"] > span::text').get(),
                'posted-date': job.css('div[aria-describedby="header-postedDate"]::text').get(),
            }
