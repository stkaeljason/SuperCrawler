# coding:utf-8

#python
import json

#scrapy
import time

from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import LocTagItem
from ImageSpider.items import CityTagItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest

from ImageSpider import utils
from ImageSpider.crawl_accounts import city_crawl_list


class LocalTagSpider(RedisCrawlSpider):
    """for crawl city add country site"""
    name = 'ins_city_spider'
    redis_key = 'city_tag:start_urls'
    # start_url = 'https://www.instagram.com/explore/locations/EC/ecuador/'
    loc_url_format = 'https://www.instagram.com/explore/locations/{id}/{tag_name}/'
    main_headers = {
        'accept':'image/webp,image/apng,image/*,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.9',
        'referer':'https://www.instagram.com',
        'user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',

    }

    more_headers = {
        'accept': '*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.9',
        # 'content-length':6,
        'content-type':'application/x-www-form-urlencoded',
        'origin':'https://www.instagram.com',
        'referer':'https://www.instagram.com',
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',
        'x-csrftoken':'q2Fffr96AdNHVpU34U6tFw37qS3mPsH0',
        'x-instagram-ajax':1,
        'x-requested-with':'XMLHttpRequest'
    }


    # cookies_dict = {}
    #
    # def parse(self, response):
    #     login_page = 'https://www.instagram.com/'
    #     if len(self.cookies_dict) == 0:
    #         for form_data in city_crawl_list:
    #             cookiejar_name = form_data['username']
    #             print(cookiejar_name)
    #             time.sleep(2)
    #             yield Request(login_page,
    #                           meta={'cookiejar': cookiejar_name, 'profile_response': response, 'form_data': form_data},
    #                           callback=self.login, errback=self.report_error, dont_filter=True)
    #
    #     else:
    #         yield Request(response.url, meta={'profile_response': response},
    #                       callback=self.parse_main_city, errback=self.report_error, dont_filter=True)
    #
    # def login(self, response):
    #
    #     sel = Selector(response)
    #     img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
    #     img_dict = json.loads(img_data.lstrip('window._sharedData = ').rstrip(';'))
    #     self.login_headers['x-csrftoken'] = img_dict['config']['csrf_token']
    #     time.sleep(4)
    #     yield FormRequest(url='https://www.instagram.com/accounts/login/ajax/',
    #                       meta=response.meta,
    #                       headers=self.login_headers,
    #                       formdata=response.meta['form_data'],
    #                       callback=self.parse_main_city,
    #                       errback=self.report_error,
    #                       dont_filter=True,
    #                       )

    def parse(self, response):
        # print('cookies_dict', self.cookies_dict)
        # if len(self.cookies_dict) != 0:
        print('start_main_ls_ls')
        item = CityTagItem()
        # sel = Selector(response.meta['profile_response'])
        sel = Selector(response)
        city_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
        city_dict = json.loads(city_data.lstrip('window._sharedData = ').rstrip(';'))
        city_list = city_dict['entry_data']['LocationsDirectoryPage'][0]['city_list']

        x_csrftoken = city_dict['config']['csrf_token']
        self.more_headers['x_csrftoken'] = x_csrftoken
        # print('city_list',city_list)
        for city in city_list:
            item['loc_city_name'] = city['slug']
            item['loc_city_id'] = city['id']
            # item['loc_parent_name'] = 'ecuador'
            # item['loc_parent_id'] = 'EC'
            item['loc_parent_name'] = city_dict['entry_data']['LocationsDirectoryPage'][0]['country_info']['slug']
            item['loc_parent_id'] = city_dict['entry_data']['LocationsDirectoryPage'][0]['country_info']['id']
            item['city_country_name'] = city_dict['entry_data']['LocationsDirectoryPage'][0]['country_info']['name']
            item['is_crawled'] = 0
            # city_url = self.loc_url_format.format(id=item['loc_parent_id'], tag_name=item['loc_parent_name'])
            # yield Request(url=city_url, headers=self.main_headers, callback=self.parse_loc_tag, meta={'item':item})
            yield item
        self.log('finish the first city page')
        # 从首页开始获取更多页
        next_num = city_dict['entry_data']['LocationsDirectoryPage'][0]['next_page']
        if next_num == 2:
            # yield FormRequest(url='https://www.instagram.com/explore/locations/{}/'.format(item['loc_parent_id']),
            #                   formdata={'page':str(next_num)},
            #                   headers= self.more_headers,
            #                   callback=self.parse_more_city,
            #                   meta={'page':next_num},
            #                   errback=self.report_error
            #
            #                   )
            yield Request(url=response.url,
                              headers=self.main_headers,
                              callback=self.parse_more_city,
                              meta={'page': next_num},
                              errback=self.report_error

                              )

    # def parse_more_city(self, response):
    #     item = CityTagItem()
    #     city_data = json.loads(response.body)
    #     for city in city_data['city_list']:
    #         item['loc_city_name'] = city['slug']
    #         item['loc_city_id'] = city['id']
    #         # item['loc_parent_name'] = 'ecuador'
    #         # item['loc_parent_id'] = 'EC'
    #         item['loc_parent_name'] = city_data['country_info']['slug']
    #         item['loc_parent_id'] = city_data['country_info']['id']
    #         item['city_country_name'] = city_data['country_info']['name']
    #         item['is_crawled'] = 0
    #         # city_url = self.loc_url_format.format(id=item['loc_parent_id'], tag_name=item['loc_parent_name'])
    #         # yield Request(url=city_url, headers=self.main_headers, callback=self.parse_loc_tag, meta={'item': item})
    #         yield item
    #     self.log('finish the  city page: %s'%(response.meta['page']))
    #
    #     if city_data['next_page'] != None:
    #         yield FormRequest(url='https://www.instagram.com/explore/locations/{}/'.format(item['loc_parent_id']),
    #                           formdata={'page': str(city_data['next_page'])},
    #                           headers=self.more_headers,
    #                           callback=self.parse_more_city,
    #                           meta={'page':city_data['next_page']},
    #                           errback=self.report_error
    #                     )
    def parse_more_city(self, response):
        item = CityTagItem()
        with open('./city_data.json', 'r') as f:
            city_data_list = f.readlines()
            for city_data in city_data_list:
                city_data = json.loads(city_data)
                for city in city_data['city_list']:
                    item['loc_city_name'] = city['slug']
                    item['loc_city_id'] = city['id']
                    # item['loc_parent_name'] = 'ecuador'
                    # item['loc_parent_id'] = 'EC'
                    item['loc_parent_name'] = city_data['country_info']['slug']
                    item['loc_parent_id'] = city_data['country_info']['id']
                    item['city_country_name'] = city_data['country_info']['name']
                    item['is_crawled'] = 0
                    yield item
            self.log('finish the  city crawl')

    def report_error(self, failure):
        utils.send_mail(repr(failure.value.response)+repr(failure.value), self.name, 'jason', 'crawl_exception')

