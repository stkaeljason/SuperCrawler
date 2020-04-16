# coding:utf-8

# scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import CarImEntranceItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest

from ImageSpider.custom_settings import custom_settings_for_aicar


class CollCarBrand(RedisCrawlSpider):
    """收集汽车的图库入口url"""
    name = 'aicar_coll_cn_'
    redis_key = 'aicar_coll'
    custom_settings = custom_settings_for_aicar

    def parse(self, response):
        sel  = Selector(response)
        brand_list = sel.xpath('//li[@nodetype="menu"]')
        for brand in brand_list:
            brand_url_pis = brand.xpath('.//a/@href').extract()[0]
            brand_name = brand.xpath('.//a/text()').extract()[0].encode('utf8')
            brand_url = 'http://newcar.xcar.com.cn' + brand_url_pis
            yield Request(brand_url, meta={'brand_name':brand_name}, callback=self.parse_series)

    def parse_series(self, response):
        item = CarImEntranceItem()
        item['entran_brand'] = response.meta['brand_name']
        sel = Selector(response)
        series_list = sel.xpath('//li[@class="menu_li"]')
        for series in series_list:
            series_url_pis = series.xpath('.//a/@href').extract()[0]
            item['entran_im_url'] = 'http://newcar.xcar.com.cn' + series_url_pis
            item['entran_series'] = series.xpath('.//a/@title').extract()[0]
            item['entran_series_id'] = series.xpath('.//a/@id').extract()[0]
            yield item
