# -*- coding: utf-8 -*-
import urllib.parse as urlparse
from urllib.parse import urlencode
import scrapy
import json
import logging


class FtstckSpider(scrapy.Spider):
    name = 'ftstck'
    allowed_domains = ['footstock.com']
    start_urls = ['https://www.footstock.com/api/cards?page=0&sort=score,desc&withSellPrice=true']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        'TELNETCONSOLE_ENABLED': False,
        'CONCURRENT_REQUESTS': 16,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    def parse(self, response):
        cards = json.loads(response.body_as_unicode())['cards']
        if cards:
            for card in cards:
                result = dict()
                result['Player Name'] = card['playerName']
                result['Club'] = card['club']
                result['Buy this card'] = card['orderPrices']['currentSellPrice']
                result['Sell this card'] = card['orderPrices']['currentBuyPrice']
                result['Last card deal'] = card['orderPrices']['lastPrice']
                yield result

            url_parts = list(urlparse.urlparse(response.request.url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            query.update({'page': int(query.get('page'))+1})
            url_parts[4] = urlencode(query)
            next_page = urlparse.urlunparse(url_parts)

            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
