# coding:utf-8

# python
import json
import time
import random
import socket
import copy

# scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import InsTagItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from ImageSpider.settings import TAG_IMAGE_NUM_LIMIT

# jason
from ImageSpider import utils


class InsTagSpider(RedisCrawlSpider):
    name = 'ins_im_tag_spider'
    redis_key = 'ins_tag:start_urls'
    account_list = []
    # start_url = 'https://www.instagram.com/explore/locations/EC/ecuador/'
    # user_profile_url_format = 'https://www.instagram.com/{username}/'
    tag_profile_url_format = 'https://www.instagram.com/explore/tags/{tagname}/'
    more_img_format = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables=%7B%22tag_name%22%3A%22{tag_name}%22%2C%22show_ranked%22%3Afalse%2C%22first%22%3A8%2C%22after%22%3A%22{end_cursor}%22%7D'
    query_hash = 'f92f56d47dc7a55b606908374b43a314'
    main_headers = {
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.instagram.com',
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',

    }

    more_headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.instagram.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',
        'upgrade-insecure-requests': 1,
        'cookie': '''mid=WremtgAEAAEbtjQeUkNJo8mL6MKX; fbm_124024574287414=base_domain=.instagram.com; ig_pr=1; ig_vh=678; ig_or=landscape-primary; ig_vw=783; csrftoken=f1ZJMhZS4cvMSykWY5ExjorzWlKDf8If; ds_user_id=7370940409; sessionid=IGSC0a54ffbaa8a8a582255ea79fed5ab63f3d8609dc30cce8704479f8b855c4a8f0%3AKVe3cZcbuMgrZab2nu6GGztKy9keaIsY%3A%7B%22_auth_user_id%22%3A7370940409%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%227370940409%3AmcFzJKgJGZlmOm2dzEHEKKa4q41jfEpB%3Aedc481b7b9237817d4161ce9759dccbce8fcee80668d8f73168d79805207a767%22%2C%22last_refreshed%22%3A1523342089.0092294216%7D; rur=ATN; fbsr_124024574287414=s8QyXK6VNlmYiJQc0iKAdFr15Tt1b9ocxGe_NMUoniE.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURYQ2U1ZHB3d0VYV285RFBGRW5oNk5rT1hWX0l2N056S2NpN0hYU0d0dHM1TUs1SV83Y3NkUTdOdjVCbXNfalg4ckRvSjl1Q28wSjZaT3hzY3VqWl9ucGpvcjhaNnQtazBiYjc0VzhtY0Q4TkRTWDVkWkR2S0tEZzhpLVZKMTE1dl92Qjcwa25OcDhMWV80Z2stTmFrNmVqeG5BZ2lITWR1WGUzRGdtRnpGSF9BTFozekdDano3SXgyd3pIU002cWlEOW1SU0RNTzFOU0VPWUpvNlAzZE5IZ0hwN1Jtek1kQUJRTUF0dlFlQ3NIdHVCRUFWb2EtNTYyZ1V5dVd5QVdCaDhrN1NHQS1hVkRUdFhGTzFsTVBsQXNQSmliem9yTjc0RGhmb1paMDQtVUZVTUhzNFpsNXgyd09qbTRhNTVRUEJFWmpodGF3QkNCS2UtUXJncTdpdyIsImlzc3VlZF9hdCI6MTUyMzM0MjA5MiwidXNlcl9pZCI6IjEwMDAyNTE3Mzc1MTU4NiJ9; urlgen="{\"time\": 1523324328\054 \"192.155.86.108\": 63949}:1f5mrl:rLLcwkoCIKamfosER2PJApTDkYM"''',
        # 'x-requested-with': 'XMLHttpRequest'
    }

    attempt_headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com',
        'x-csrftoken': 'NzoRNJ1qvkKvZ3pbJBvSSgXlzZA9lrOK',
        'x-instagram-ajax': 1,
        'x-requested-with': 'XMLHttpRequest'

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
    user_im_sum = 0

    def parse(self, response):
        self.user_im_sum = 0
        login_page = 'https://www.instagram.com/'
        if len(self.cookies_dict) == 0:
            for account in self.account_list:

                cookiejar_name = account['username']
                self.log(cookiejar_name)
                time.sleep(3)
                yield Request(login_page,
                           meta={'cookiejar': cookiejar_name,  'profile_response': response,'formdata': account},
                           callback=self.login, errback=self.report_error, dont_filter=True)
        else:
            self.log('request % again'%response.url)
            yield Request(response.url,meta={'profile_response': response},
                           callback=self.parse_main_page, errback=self.report_error, dont_filter=True)


    def login(self, response):
        sel = Selector(response)
        img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
        img_dict = json.loads(img_data.lstrip('window._sharedData = ').rstrip(';'))
        self.login_headers['x-csrftoken'] = img_dict['config']['csrf_token']
        time.sleep(7)
        return FormRequest(url='https://www.instagram.com/accounts/login/ajax/',
                           meta=response.meta,
                           headers=self.login_headers,
                           formdata=response.meta['formdata'],
                           callback=self.parse_main_page,
                           errback=self.report_error,
                           dont_filter=True,
                           )


    def parse_main_page(self, response):

        if len(self.cookies_dict) > 0:
            item = InsTagItem()
            sel = Selector(response.meta['profile_response'])
            img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
            img_dict = json.loads(img_data.lstrip('window._sharedData = ').rstrip(';'))
            tag_info = img_dict['entry_data']['TagPage'][0]['graphql']['hashtag']
            img_list = tag_info['edge_hashtag_to_media']['edges']
            img_count = tag_info['edge_hashtag_to_media']['count']
            item['tag_id'] = tag_info['id']

            self.main_headers['referer'] = self.tag_profile_url_format.format(tagname=tag_info['name'])
            self.more_headers['referer'] = self.tag_profile_url_format.format(tagname=tag_info['name'])
            # self.more_headers['x-instagram-gis'] = hashlib.md5('guayaquil-ecuador'+str(int(time.time())).encode('utf-8')).hexdigest()

            if img_count > 40:
                for img in img_list:
                    if img['node']['__typename'] != 'GraphVideo':
                        item['img_id'] = img['node']['id']
                        item['tag_id'] = tag_info['id']
                        item['tag_name'] = tag_info['name']
                        item['img_url'] = img['node']['thumbnail_src']
                        # item['img_data'] = json.dumps(img_dict)
                        self.user_im_sum += 1
                        yield Request(item['img_url'],
                                      callback=self.get_img_content,
                                      meta={'item':item},
                                      headers=self.main_headers,
                                      errback=self.report_error)

                # time.sleep(1)

                has_next_page = tag_info['edge_hashtag_to_media']['page_info']['has_next_page']
                end_cursor = tag_info['edge_hashtag_to_media']['page_info']['end_cursor']
                if has_next_page:
                    url = self.more_img_format.format(query_hash=self.query_hash,
                                                      tag_name=item['tag_name'],
                                                      end_cursor=end_cursor
                                                      )
                    yield Request(url,
                                  callback=self.parse_more_page,
                                  headers=self.more_headers,
                                  meta={'tag_id': item['tag_id'],
                                        'tag_name': item['tag_name'],
                                        'img_count': img_count,
                                        # 'cookiejar': random.choice(self.cookie_list)
                                        },
                                  errback=self.report_error,
                                  dont_filter=True
                                  )
            else:
                self.log('*********** finish user:%s  for <40 count***********' % (item['tag_name']))
                # set_crawled(item['img_owner_id'], int(img_count), int(time.time()))

    def parse_more_page(self, response):
        item = InsTagItem()
        img_data = json.loads(response.body)
        img_list = img_data['data']['hashtag']['edge_hashtag_to_media']['edges']
        img_count = img_data['data']['hashtag']['edge_hashtag_to_media']['count']

        # time.sleep(100)  # test

        for img in img_list:
            if img['node']['__typename'] != 'GraphVideo':
                item['img_id'] = img['node']['id']
                item['tag_id'] = response.meta['tag_id']
                item['tag_name'] = response.meta['tag_name']
                item['img_url'] = img['node']['thumbnail_src']
                # item['img_data'] = json.dumps(img_data)
                self.user_im_sum += 1
                yield Request(item['img_url'],
                              callback=self.get_img_content,
                              meta={'item': item,
                                    },
                              headers=self.main_headers,
                              errback=self.report_error
                              )

        has_next_page = img_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        end_cursor = img_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        if self.user_im_sum < TAG_IMAGE_NUM_LIMIT:
            if has_next_page:
                url = self.more_img_format.format(query_hash=self.query_hash,
                                                  tag_name=item['tag_name'],
                                                  end_cursor=end_cursor
                                                  )
                # response.meta['cookiejar'] = random.choice(self.cookie_list)
                yield Request(url,
                              callback=self.parse_more_page,
                              headers=self.more_headers,
                              meta=response.meta,
                              errback=self.report_error,
                              dont_filter=True
                              )
                time.sleep(0.5)

            else:
                self.log('*********** finish user:%s ***********' % (response.meta['tag_name']))
                    # set_crawled(item['img_owner_id'], response.meta['img_count'], int(time.time()))
        else:
            self.log('*********** finish user:%s ***********' % (response.meta['tag_name']))
        #     # set_crawled(item['img_owner_id'], IMAGE_NUM_LIMIT, int(time.time()))

    def get_img_content(self, response):
        item = response.meta['item']
        item['img_content'] = response.body
        yield item

    def report_error(self, failure):
        if failure.value.response.status != 404 and failure.value.response.status != 500:
            utils.send_mail(self.name+'__'+socket.gethostname() + '__' + repr(failure.value.response), self.name, 'jason',
                        'crawl_exception')
        # print(failure.value.response.status,type(failure.value.response.status),failure.value.response)
        # if failure.value.response.status == 429:
        #     time.sleep(100)
