# -*- coding: utf-8 -*-
import scrapy


class FtstckSpider(scrapy.Spider):
    name = 'ftstck'
    allowed_domains = ['footstock.com']
    start_urls = ['http://footstock.com/']

    def parse(self, response):
        pass
