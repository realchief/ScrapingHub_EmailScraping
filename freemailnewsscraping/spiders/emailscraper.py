from scrapy.conf import settings
from scrapy import Request

import scrapy
from scrapy.item import Item, Field


class SiteProductItem(Item):
    Email = Field()


class EmailScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['freemailnews.com']
    START_URL = 'http://freemailnews.com/emaillistings'
    pagination = 'http://freemailnews.com/emaillistings/{page_num}'
    settings.overrides['ROBOTSTXT_OBEY'] = False

    def start_requests(self):
        yield Request(url=self.START_URL,
                      callback=self.parse_page,
                      dont_filter=True
                      )

    def parse_page(self, response):
        for page_num in range(0, 372317):
            sub_link = self.pagination.format(page_num=page_num)
            yield Request(url=sub_link, callback=self.parse_email, dont_filter=True)

    def parse_email(self, response):
        result_email = SiteProductItem()
        li_list = response.xpath("//li/text()").extract()
        for li in li_list:
            email = li.replace('-', '').encode('utf-8')
            result_email['Email'] = email
            yield result_email


