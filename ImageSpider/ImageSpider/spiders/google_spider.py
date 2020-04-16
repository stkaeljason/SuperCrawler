# coding:utf-8

# python
import json
import time
import random
import socket
import copy
import re

# scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import GoogleImItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest

from ImageSpider import utils
from urllib import parse
from ImageSpider.custom_settings import custom_settings_for_google

class GoogleSpider(RedisCrawlSpider):
    name = 'google_im_spider'
    redis_key = 'google_im:start_urls'
    gg_key = 'default_gg_im'
    start_url = 'https://images.google.com/'
    custom_settings = custom_settings_for_google
    headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en - US, en;q = 0.9',
    'referer':'https://www.google.com/',
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36'
    }
    im_headers = {
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en - US, en;q = 0.9',
        'referer': 'https://www.google.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36'
    }

    def parse(self, response):
        key_pattern = re.compile(r'&q=(?P<query_key>.*?)&')
        img_lable = re.search(key_pattern, response.url).group('query_key').replace('+', '_')
        # print('gg_key',self.gg_key)
        sel = Selector(response)
        img_list = sel.xpath('//div[@class="rg_meta notranslate"]/text()')
        # print('+++++img_list+++++',img_list)
        if img_list:
            image_item = GoogleImItem()
            for img in img_list:
                # print('source:',json.loads(img.extract()))
                img_json = json.loads(img.extract())
                if img_json.__contains__('ou'):
                    image_item['img_id'] = img_json['id'].strip('-: ')
                    image_item['img_url'] = img_json['ou']
                    image_item['img_lable'] = img_lable
                    # print(image_item)
                    if image_item['img_url'].endswith(('.jpg', '.png', '.JPG')):
                        url=''
                        if 'http://' in image_item['img_url']:
                            url=image_item['img_url'].replace('http://','https://')
                        else:
                            url=image_item['img_url']
                        yield Request(url=url,meta={'item':image_item},headers=self.im_headers,
                                      callback=self.parse_image,
                                      errback=self.report_error)
            more_url = self.get_more_ulr(response.url)
            yield Request(url=more_url, headers=self.headers,
                          callback=self.parse_more,
                          errback=self.report_error)
        else:
            print('this page not has more')

    def parse_more(self, response):
        sel = Selector(response)
        img_list = sel.xpath('//div[@class="rg_meta notranslate"]/text()')
        key_pattern = re.compile(r'&q=(?P<query_key>.*?)&')
        img_lable = re.search(key_pattern, response.url).group('query_key').replace('+', '_')
        if img_list:
            image_item = GoogleImItem()
            for img in img_list:
                img_json = json.loads(img.extract())
                if img_json.__contains__('ou'):
                    image_item['img_id'] = img_json['id'].strip(':')
                    image_item['img_url'] = img_json['ou']
                    image_item['img_lable'] = img_lable
                    if image_item['img_url'].endswith(('.jpg','.png','.JPG')):
                        url = ''
                        if 'http://' in image_item['img_url']:
                            url = image_item['img_url'].replace('http://', 'https://')
                        else:
                            url=image_item['img_url']
                        yield Request(url=url, meta={'item':image_item}, headers=self.im_headers,
                                      callback=self.parse_image,
                                      errback=self.report_error)

            more_url = self.get_more_ulr(response.url)
            yield Request(url=more_url, headers=self.headers,
                          callback=self.parse_more,
                          errback=self.report_error)
            time.sleep(1)
        else:
            print('this page not has more')

    def parse_image(self, response):
        image_item = response.meta['item']
        image_item['img_content'] = response.body
        yield image_item

    def report_error(self, failure):
        if failure.value.response.status != 404 and failure.value.response.status != 500:
            utils.send_mail(self.name+'__'+socket.gethostname() + '__' + repr(failure.value.response), self.name,
                        'jason',
                        'crawl_exception')

    def get_more_ulr(self, res_url):
        ijn_pattern = re.compile(r'&ijn=(?P<ijn>.*?)&')
        ijn_str = re.search(ijn_pattern, res_url).group()
        ijn_num = int(re.search(ijn_pattern, res_url).group('ijn'))
        # print('ijn_num', ijn_num)
        start_pattern = re.compile(r'&start=(?P<start>.*?)&')
        start_str = re.search(start_pattern, res_url).group()
        more_url = res_url.replace(ijn_str, '&ijn={}&'.format(ijn_num + 1)).replace(start_str, '&start={}&'.format(
            (ijn_num + 1) * 100))
        # print('++++++++more_url++++++++', more_url)
        return more_url

