# -*- coding: utf-8 -*-
import scrapy
from ua.items import UaItem

class UalistSpider(scrapy.Spider):
    name = 'ualist'
    allowed_domains = ['udger.com']
    start_urls = ['https://udger.com/resources/ua-list#Browser']

    def parse(self, response):
        item = UaItem()
        item['browser'] = response.xpath('//tr//a[contains(@href, "/resources/ua-list/browser-detail?")]/text()').extract()
        item['useragent_link'] = response.xpath('//tr//a[contains(@href, "/resources/ua-list/browser-detail?")]/@href').extract()
        yield item
