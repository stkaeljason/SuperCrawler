# coding:utf-8

# scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import CarPicItem
from scrapy.selector import Selector
from scrapy.http import Request

from ImageSpider.models.aicar_entrance import aicar_setcrawled_base_series_id
from ImageSpider.utils import  xpath_exception_alarm, exception_alarm

from ImageSpider.custom_settings import custom_settings_for_aicar


class CarImageSpider(RedisCrawlSpider):
    """汽车图片爬虫"""

    name = 'aicar_spider'
    redis_key = 'aicar'
    custom_settings = custom_settings_for_aicar
    # allow_domains = ['www.car.autohome.com.cn']
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/*,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'newcar.xcar.com.cn',
               'Upgrade-Insecure-Requests': 1,
               }

    image_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'img1.xcarimg.com',
        'Upgrade-Insecure-Requests': 1,
    }

    host_page = 'http://newcar.xcar.com.cn'

    # @exception_alarm
    def parse(self, response):
        """解析更多页面url"""
        sel = Selector(response)
        car_pic_page = sel_xpath(sel, '//span[@class="more"][1]/a/@href', self.name+'_'+'parse').extract()[0]
        series_id = response.url.strip('/').split('/')[-1]
        if 'car.m.autohome' not in response.url:           # 表示没有重定向
            yield Request(url=self.host_page+car_pic_page, meta={'series_id':series_id}, callback=self.crawl_image_list,dont_filter=True)
        else:
            aicar_setcrawled_base_series_id(series_id, 0)
            print('************request被重定向，is_crawled置为0***************')

    # @exception_alarm
    def crawl_image_list(self, response):
        """获取单张图片主页url列表"""
        sel = Selector(response)
        print('metaxx',response.meta)
        series_id = response.meta['series_id']
        xpath_rule = '//div[@class="pic-con"]/dl[@class="item"]/dt/a/@href'
        car_image_list = sel.xpath(xpath_rule).extract()
        if car_image_list:
            for car_image_page in car_image_list:
                car_image_url = self.host_page+car_image_page
                yield Request(url=car_image_url, headers=self.headers, callback=self.crawl_image_info)
        else:
            print('************car_image_list 空***************')

        try:
            next_page = sel.xpath('//a[contains(text(),"下一页")]/@href').extract()[0]
        except IndexError:
            print('************没有下一页了***************')
            next_page = 'javascript:void(0);'

        if 'javascript:void(0);' not in next_page:
            next_page_url = self.host_page+next_page
            yield Request(url=next_page_url, headers=self.headers, meta=response.meta, callback=self.crawl_image_list,dont_filter=True)
        else:
            aicar_setcrawled_base_series_id(series_id, 1)
            print('set is_crawl 1',series_id)

    # @exception_alarm
    def crawl_image_info(self, response):
        """在单张图片主页解析图片信息，并获取图片content"""
        sel = Selector(response)
        item = CarPicItem()
        car_brand = sel.xpath('//div[@class="place"]/a[3]/text()').extract()[0]
        car_series = sel.xpath('//div[@class="place"]/a[4]/text()').extract()[0]
        car_img_src = sel.xpath('//ul[@class="play_img"]/li/img/@src').extract()[0]

        item['car_model'] = car_brand + "_"+car_series
        item['pic_id'] = car_img_src.split('/')[-1].split('.')[0]
        car_img_url = car_img_src
        self.image_headers['Host'] = car_img_src.split('/')[2]
        # print('hosthost_imageimage**', self.image_headers['Host'])
        yield Request(car_img_url, headers=self.image_headers, callback=self.crawl_image_content, meta={'item': item})

    def crawl_image_content(self, response):
        item = response.meta['item']
        item['pic_content'] = response.body
        yield item


@xpath_exception_alarm
def sel_xpath(sel, xpath_rule, xpath_object):
    xpath_result = sel.xpath(xpath_rule)
    return xpath_result