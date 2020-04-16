# coding:utf-8

# scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.selector import Selector
from ImageSpider.items import YiPeiItem
from ImageSpider.custom_settings import custom_settings_for_yipeisite
from ImageSpider.models.yipei_model import update_is_crawl


class YiPeiSpider(RedisCrawlSpider):
    """get yipei car info"""
    name = 'yipei_spider_cn_'
    redis_key = 'yipei_site'
    custom_settings = custom_settings_for_yipeisite

    def parse(self, response):
        import json
        # sel = Selector(response)
        # res = json.loads(response)
        # code = res['code']
        # if code == 1:
        # data = res['data']['model_list'][0]
        data = response.text
        yipei_item = YiPeiItem()
        vin = response.url.split('=')[1].strip('&user')
        yipei_item['car_vin'] = vin
        yipei_item['car_vin_alias'] = vin[:8]
        yipei_item['car_data'] = data
        # car_obj_list = sel.xpath('//table[@class="MarkDiff"][1]/tbody/tr[@class="MarkDiffTr"]/td')
        #
        # car_number = response.url.split("keyword=")[1].strip('&captoken=')
        # if not car_obj_list:
        #     yipei_item['car_brand'] = ''
        #     yipei_item['car_series'] = ''
        #     yipei_item['car_made_date'] = ''
        #     yipei_item['car_number'] = car_number
        #     yipei_item['is_crawled'] = 1
        # else:
        #     yipei_item['car_brand'] = car_obj_list[0].xpath('.//text()').extract()[0]
        #     yipei_item['car_series'] = car_obj_list[2].xpath('.//text()').extract()[0]
        #     yipei_item['car_made_date'] = car_obj_list[3].xpath('.//text()').extract()[0]
        #     yipei_item['car_number'] = car_number
        #     yipei_item['is_crawled'] = 1
        update_is_crawl(vin, 1)
        yield yipei_item