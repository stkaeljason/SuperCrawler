# python
import json
import time
import random
import socket
import copy
import re

# scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest

from ImageSpider import utils
from urllib import parse

class GoogleUrlColler(RedisCrawlSpider):
    name = 'google_coll_spider'
    redis_key = 'google_coll:start_urls'
    gg_key = None
    start_url = 'https://images.google.com/'
    headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en - US, en;q = 0.9',
    'referer':'https://www.google.com/',
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36'
    }

    def parse(self, response):
        key_pattern = re.compile(r'&q=(?P<query_key>.*?)&')
        self.gg_key = re.search(key_pattern, response.url).group('query_key').replace('+', '_')
        print('gg_key',self.gg_key)
        sel = Selector(response)
        img_list = sel.xpath('//div[@class="rg_meta notranslate"]/text()')
        # print('+++++img_list+++++',img_list)
        if img_list:
            for img in img_list[:15]:
                # print('source:',json.loads(img.extract()))
                img_json = json.loads(img.extract())