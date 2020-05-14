# coding:utf-8

# python
import json

# scrapy
import time
from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import ImgUserItem
# from items import ImgUserItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest

# jason
# from ImageSpider.models.location_tag_model import get_img_loc
from ImageSpider import utils
from ImageSpider.models.location_tag_model import loc_set_crawled
# from ImageSpider.db import user_crawl_list
from ImageSpider.crawl_accounts import user_crawl_list

class ImgUserSpider(RedisCrawlSpider):
    name = 'ins_im_users_spider'
    redis_key = 'img_user:start_urls'
    loc_url_format = 'https://www.instagram.com/explore/locations/{id}/{tag_name}/'
    next_page_format='https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables=%7B%22id%22%3A%2213450033%22%2C%22first%22%3A12%2C%22after%22%3A%22{end_cursor}%22%7D'
    short_pic_format = 'https://www.instagram.com/p/{shortcode}/?taken-at={loc_id}'
    main_headers = {
        'accept':'image/webp,image/apng,image/*,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.9',
        'referer':'https://www.instagram.com',
        'user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',
    }

    more_img_headers = {
        'accept':'image/webp,image/apng,image/*,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.9',
        'referer':'https://www.instagram.com',
        'user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',
        'x-requested-with':'XMLHttpRequest'
    }

    login_headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com',
        'x-csrftoken': '',
        # 'x-instagram-ajax': 1,
        'x-requested-with': 'XMLHttpRequest',
        'x-instagram-ajax':'cc6f59f85f33',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR2YuvekAxUlhQIFufQIkIkZrwHxjMCf2ahd6umqU7TX-HUx'
    }

    cookies_dict = {}
    profile_response = None
    user_crawl_limit = 70
    user_count = 0

    def parse(self, response):
        login_page = 'https://www.instagram.com/accounts/login/'
        self.profile_response = response
        self.user_count = 0
        if len(self.cookies_dict) == 0:
            for form_data in user_crawl_list:
                cookiejar_name = form_data['username']
                print(cookiejar_name)
                time.sleep(3)
                yield Request(login_page, meta={'cookiejar':cookiejar_name, 'form_data':form_data},callback=self.login,errback=self.report_error,dont_filter=True)

        else:
            yield Request(response.url,
                           callback=self.parse_main_loc, errback=self.report_error, dont_filter=True)

    def login(self,response):

        sel = Selector(response)
        img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
        img_dict = json.loads(img_data.lstrip('window._sharedData = ').rstrip(';'))
        self.login_headers['x-csrftoken'] = img_dict['config']['csrf_token']
        time.sleep(5)
        yield FormRequest(url='https://www.instagram.com/accounts/login/ajax/',
                         meta=response.meta,
                         headers=self.login_headers,
                         formdata=response.meta['form_data'],
                         callback=self.parse_main_loc,
                         errback=self.report_error,
                         dont_filter=True,
                                         )

    def parse_main_loc(self,response):
        # item = ImgUserItem()
        if len(self.cookies_dict) >2:
            # sel = Selector(response.meta['profile_response'])
            sel = Selector(self.profile_response)
            img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
            img_dict = json.loads(img_data.lstrip('window._sharedData = ').rstrip(';'))
            # print('testest_response______________+++++++++++++')
            img_list = img_dict['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['edges']
            user_country_name = img_dict['entry_data']['LocationsPage'][0]['graphql']['location']['directory']['country']['name']
            if not img_list:
                print('have no post')
            for img in img_list:
                shortcode = img['node']['shortcode']
                loc_id = img_dict['entry_data']['LocationsPage'][0]['graphql']['location']['id']
                short_pic_url = self.short_pic_format.format(shortcode=shortcode,loc_id=loc_id)
                # print('testlsdlsd&&&&&&&----->',shortcode)
                self.user_count += 1
                yield Request(short_pic_url, callback=self.parse_user_info, meta={'user_country_name':user_country_name}, headers=self.main_headers,
                              errback=self.report_error)

            has_next_page =img_dict['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['page_info']['has_next_page']

            if has_next_page:
                end_cursor = img_dict['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['page_info']['end_cursor']
                url = self.next_page_format.format(query_hash='951c979213d7e7a1cf1d73e2f661cbd1', end_cursor=end_cursor)
                yield Request(url,callback=self.parse_morsepage,
                              meta={'user_country_name': user_country_name},
                              headers=self.more_img_headers,
                              errback=self.report_error)

    def parse_morsepage(self,response):
        img_dict = json.loads(response.body)
        img_list = img_dict['data']['location']['edge_location_to_media']['edges']
        if not img_list:
            print('wo bugubugbug')
        for img in img_list:
            shortcode = img['node']['shortcode']
            loc_id = img_dict['data']['location']['id']
            short_pic_url = self.short_pic_format.format(shortcode=shortcode, loc_id=loc_id)
            self.user_count += 1
            yield Request(short_pic_url, callback=self.parse_user_info, meta=response.meta, headers=self.main_headers,
                          errback=self.report_error)

        has_next_page = img_dict['data']['location']['edge_location_to_media']['page_info']['has_next_page']

        if self.user_count < self.user_crawl_limit:
            if has_next_page:
                end_cursor = img_dict['data']['location']['edge_location_to_media']['page_info']['end_cursor']
                url = self.next_page_format.format(query_hash='951c979213d7e7a1cf1d73e2f661cbd1', end_cursor=end_cursor)
                self.user_count += 1
                yield Request(url, callback=self.parse_morsepage,
                              meta=response.meta,
                              headers=self.more_img_headers,
                              errback=self.report_error)
                time.sleep(2.0)
            else:
                print('+++++++fininsh this user no next+++++++')
                loc_set_crawled(img_dict['data']['location']['id'], is_crawled=1)
        else:
            print('+++++++fininsh this user+++++++')
            loc_set_crawled(img_dict['data']['location']['id'],is_crawled=1)

    def parse_user_info(self,response):
        """pase userid username"""
        item = ImgUserItem()
        sel = Selector(response)
        # img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
        try:
            img_data = sel.xpath('//script[contains(text(),"window.__additionalDataLoaded")]/text()').extract()[1]
            x_index = img_data.index('{')
            json_data = img_data[x_index:-1].rstrip(')')
            img_dict = json.loads(json_data)
            user_info = img_dict['graphql']['shortcode_media']['owner']
        except IndexError:
            img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
            x_index = img_data.index('{')
            json_data = img_data[x_index:-1].rstrip(';')
            # json_data = img_data.lstrip('window._sharedData = ').rstrip(';')
            img_dict = json.loads(json_data)
            user_info = img_dict['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']
        # json_data = img_data.lstrip('window.__additionalDataLoaded').rstrip(';')
        # x_index = img_data.index('{')
        # json_data = img_data[x_index:-1].rstrip(')')
        # img_dict = json.loads(json_data)
        # user_info = img_dict['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']

        item['img_user_id'] = user_info['id']
        item['img_user_name'] = user_info['username']
        item['user_profile_url'] = response.url
        item['user_country_name'] = response.meta['user_country_name']
        item['is_crawled'] = 0
        # print('tesitetstsetes88888888888888')
        yield item

    def report_error(self, failure):
        utils.send_mail(repr(failure.value.response), self.name, 'jason', 'crawl_exception')