# coding:utf-8

# python
import json
import time
import random
import socket
import copy


# scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import CarImEntranceItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest


class CollCarBrand(RedisCrawlSpider):
    """收集汽车的图库入口url"""
    name = 'car_entrance_coll_cn_'
    redis_key = 'homeofcar_coll'

    def parse(self, response):
        item = CarImEntranceItem()
        sel  = Selector(response)
        # image_coll_list = sel.xpath('//a[contains(text(),"图库")]/@href').extract()
        # for image_coll in image_coll_list:
        #     item['entran_im_url'] = 'https:'+image_coll
        #     yield item
        car_list = sel.xpath('//dl')
        print('car_len',len(car_list))
        for car in car_list:
            item['entran_brand'] = car.xpath('.//dt/div/a/text()').extract()[0].encode('utf8')
            image_ul_list = car.xpath('.//dd/ul[@class="rank-list-ul"]')
            print('image_ul_list',len(image_ul_list))
            for ul in image_ul_list:
                image_coll_list = ul.xpath('.//li')
                for coll in image_coll_list:
                    try:
                        item['entran_im_url'] = 'https:' + coll.xpath('.//a[contains(text(),"图库")]/@href').extract()[0].split('#')[0]
                    except IndexError:
                        continue
                    item['entran_series'] = coll.xpath('.//h4/a/text()').extract()[0].encode('utf8')
                    item['entran_series_id'] = item['entran_im_url'].split('/')[-1].strip('.html')
                    item['entran_main_url'] = 'https:' + coll.xpath('.//h4/a/@href').extract()[0]

                    # print(item)
                    yield item