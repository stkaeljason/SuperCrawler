# coding:utf-8

#python
import json

#scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import LocTagItem
from ImageSpider.items import CityTagItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest

from ImageSpider.models.loc_city_model import city_set_crawled

from ImageSpider import utils


class LocalTagSpider(RedisCrawlSpider):
    name = 'ins_location_spider'
    redis_key = 'ins_loc:start_urls'
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
        # 'referer':'https://www.instagram.com/explore/locations/EC/ecuador/',
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',
        'x-csrftoken':'vABNBMZNuy95qawRo1Y8TCEp5L9nJydI',
        'x-instagram-ajax':1,
        'x-requested-with':'XMLHttpRequest'
    }


    def parse(self,response):
        item = LocTagItem()
        sel = Selector(response)
        img_loc_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
        img_loc_dict = json.loads(img_loc_data.lstrip('window._sharedData = ').rstrip(';'))
        img_loc_list = img_loc_dict['entry_data']['LocationsDirectoryPage'][0]['location_list']

        # update headers
        x_csrftoken = img_loc_dict['config']['csrf_token']
        self.more_headers['x-csrftoken'] = x_csrftoken
        city_id = img_loc_dict['entry_data']['LocationsDirectoryPage'][0]['city_info']['id']
        city_name = img_loc_dict['entry_data']['LocationsDirectoryPage'][0]['city_info']['slug']

        self.log('**************************start the city:%s**************************' % (city_id))
        for loc in img_loc_list:
            item['loc_tag_name'] = loc['slug']
            item['loc_id'] = loc['id']
            item['loc_parent_name'] = city_name
            item['loc_parent_id'] = city_id
            item['loc_country_name'] = img_loc_dict['entry_data']['LocationsDirectoryPage'][0]['country_info']['name']
            item['is_crawled'] = 0
            yield item
        next_num = img_loc_dict['entry_data']['LocationsDirectoryPage'][0]['next_page']
        if next_num == 2:
            yield FormRequest(url='https://www.instagram.com/explore/locations/{loc_parent_id}/'.format(loc_parent_id=item['loc_parent_id']),
                              formdata={'page': str(next_num)},
                              headers=self.more_headers,
                              callback=self.parse_more_location,
                              errback=self.report_error

                              )

    def parse_more_location(self,response):
        item = LocTagItem()
        location_data = json.loads(response.body)

        city_id = location_data['city_info']['id']
        city_name = location_data['city_info']['slug']
        for location in location_data['location_list']:
            item['loc_tag_name'] = location['slug']
            item['loc_id'] = location['id']
            item['loc_parent_name'] = city_name
            item['loc_parent_id'] = city_id
            item['loc_country_name'] = location_data['country_info']['name']
            item['is_crawled'] = 0
            yield item


        if location_data['next_page'] != None:
            yield FormRequest(url='https://www.instagram.com/explore/locations/{loc_parent_id}/'.format(loc_parent_id=item['loc_parent_id']),
                              formdata={'page': str(location_data['next_page'])},
                              headers=self.more_headers,
                              callback=self.parse_more_location,
                              errback=self.report_error
                              )

        else:
            city_set_crawled(city_id)   # set is_crawled 1
            utils.send_mail('**finish the city:%s**'%(city_id), self.name, 'jason', 'crawl_city_success')
            self.log('**************************finish the city:%s**************************'%(city_id))

    def report_error(self, failure):
        utils.send_mail(repr(failure.value),self.name,'jason','crawl_exception')
