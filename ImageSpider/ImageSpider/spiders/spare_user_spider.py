# coding:utf-8

# python
import json
import redis

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
    name = 'ins_im_spare_users_spider'
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
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com',
        'x-csrftoken': '',
        'x-instagram-ajax': 1,
        'x-requested-with': 'XMLHttpRequest'
    }

    cookies_dict = {}

    def parse(self, response):
        login_page = 'https://www.instagram.com/'
        if len(self.cookies_dict) == 0:
            for form_data in user_crawl_list:
                cookiejar_name = form_data['username']
                time.sleep(3)
                yield Request(login_page, meta={'cookiejar':cookiejar_name,'profile_response':response,'form_data':form_data},callback=self.login,errback=self.report_error,dont_filter=True)

        else:
            yield Request(response.url,meta={'profile_response': response},
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
        if len(self.cookies_dict) != 0:
            sel = Selector(response.meta['profile_response'])
            # sel = Selector(response)
            img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
            img_dict = json.loads(img_data.lstrip('window._sharedData = ').rstrip(';'))
            # print('testest_response______________+++++++++++++')
            img_list = img_dict['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['edges']
            # user_country_name = img_dict['entry_data']['LocationsPage'][0]['graphql']['location']['directory']['country']['name']
            user_country_name = "kyrgyzstan"  # genju xuyao tiaozheng
            if not img_list:
                print('have no post')
            for img in img_list:
                shortcode = img['node']['shortcode']
                loc_id = img_dict['entry_data']['LocationsPage'][0]['graphql']['location']['id']
                short_pic_url = self.short_pic_format.format(shortcode=shortcode,loc_id=loc_id)
                # print('testlsdlsd&&&&&&&----->',shortcode)
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
            yield Request(short_pic_url, callback=self.parse_user_info, meta=response.meta, headers=self.main_headers,
                          errback=self.report_error)

        has_next_page = img_dict['data']['location']['edge_location_to_media']['page_info']['has_next_page']


        if has_next_page:
            end_cursor = img_dict['data']['location']['edge_location_to_media']['page_info']['end_cursor']
            url = self.next_page_format.format(query_hash='951c979213d7e7a1cf1d73e2f661cbd1', end_cursor=end_cursor)
            yield Request(url, callback=self.parse_morsepage,
                          meta=response.meta,
                          headers=self.more_img_headers,
                          errback=self.report_error)
            time.sleep(3)
        # else:
        #     loc_set_crawled(img_dict['data']['location']['id'],is_crawled=1)

    def parse_user_info(self,response):
        """pase userid username"""
        item = ImgUserItem()
        sel = Selector(response)
        img_data_list = sel.xpath('//script[contains(text(),"window.__additionalDataLoaded")]')
        img_data = img_data_list[1].xpath('.//text()').extract()[0]
        # index_start = img_data.index("\"edge_media_preview_comment\":")
        # index_end = img_data.index(",\"comments_disabled\"")
        # data = img_data.replace(img_data[0:index_num], '').strip(');')
        data = img_data.split("\"edge_media_preview_comment\":")[1]
        data = data.split(",\"comments_disabled\"")[0]
        img_dict = json.loads(data)
        try:
            user_info = img_dict['edges'][0]['node']['owner']
        except IndexError:
            data = img_data.split("\"owner\":")[1]
            data = data.split(",\"is_ad\"")[0]
            img_dict = json.loads(data)
            user_info = img_dict
        item['img_user_id'] = user_info['id']
        item['img_user_name'] = user_info['username']
        # item['full_name'] = user_info['full_name']
        item['user_profile_url'] = response.url
        item['user_country_name'] = response.meta['user_country_name']
        item['is_crawled'] = 0
        # print('tesitetstsetes88888888888888')
        yield item

    def report_error(self, failure):
        utils.send_mail(repr(failure.value.response), self.name, 'jason', 'crawl_exception')