# coding:utf-8

# python
import json
import time
import random
import socket
import copy

# scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from ImageSpider.items import ImageItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest

# jason
# from ImageSpider.models.img_user_model import get_img_user
# from ImageSpider.settings import IMAGE_NUM_LIMIT
from ImageSpider import utils
from ImageSpider.models.img_user_model import set_crawled
from ImageSpider.models.crawl_config import get_config

class ImageSpider(RedisCrawlSpider):
    name = 'ins_im_spider_jason'
    redis_key = 'ins_img:start_urls'
    account_list = []
    image_num_limit = None
    # image_save_fold = None
    # start_url = 'https://www.instagram.com/explore/locations/EC/ecuador/'
    user_profile_url_format = 'https://www.instagram.com/{username}/'
    more_img_format = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{end_cursor}%22%7D'
    query_hash = '42323d64886122307be10013ad2dcc44'
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
        # 'content - length': 6,
        # 'content-type':'application/json',
        # 'origin':'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36',
        # 'x-csrftoken': 'vABNBMZNuy95qawRo1Y8TCEp5L9nJydI',
        # 'x-instagram-ajax': 1,
        # 'x-instagram-gis':'5d077b2e2b378064a240cfd6508eba14',
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
        'x-requested-with': 'XMLHttpRequest',
        # 'X-Instagram-AJAX': 'ac5d0f89adf7',
        # 'X-IG-App-ID': '936619743392459',
        # 'X-IG-WWW-Claim': 'hmac.AR3Gl3WT587606JvGPiRZ-6hPTo94XToJ4C8s8hgPLFBl_PB'
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
        'x-requested-with': 'XMLHttpRequest',
        # 'X-Instagram-AJAX':'ac5d0f89adf7',
        # 'X-IG-App-ID': '936619743392459',
        # 'X-IG-WWW-Claim': 'hmac.AR3Gl3WT587606JvGPiRZ-6hPTo94XToJ4C8s8hgPLFBl_PB'
    }
    cookies_dict = {}
    user_im_sum = 0
    profile_response = None

    def parse(self, response):
        self.profile_response = response
        self.image_num_limit = int(get_config('ins_im_limit','ins_im_crawl'))  # 获取每个人的图片抓取量配置
        image_save_fold = get_config('ins_im_fold', 'ins_im_crawl')       # 获取人脸文件夹的保存文件夹名称
        print('image_save_fold', image_save_fold)

        self.user_im_sum = 0
        login_page = 'https://www.instagram.com/accounts/login/'
        if len(self.cookies_dict) == 0:
            for account in self.account_list:

                cookiejar_name = account['username']
                self.log(cookiejar_name)
                time.sleep(3)
                yield Request(login_page,
                           meta={'cookiejar': cookiejar_name,  'formdata': account, 'image_save_fold':image_save_fold},
                           callback=self.login, errback=self.report_error, dont_filter=True)
        else:
            self.log('request % again'%response.url)
            yield Request(response.url,meta={'image_save_fold': image_save_fold},
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

        if len(self.cookies_dict) > 2:
            item = ImageItem()
            # sel = Selector(response.meta['profile_response'])
            sel = Selector(self.profile_response)
            img_data = sel.xpath('//script[contains(text(),"window._sharedData")]/text()').extract()[0]
            img_dict = json.loads(img_data.lstrip('window._sharedData = ').rstrip(';'))
            img_user_info = img_dict['entry_data']['ProfilePage'][0]['graphql']['user']
            img_list = img_user_info['edge_owner_to_timeline_media']['edges']
            img_count = img_user_info['edge_owner_to_timeline_media']['count']
            item['img_owner_id'] = img_user_info['id']
            item['img_save_fold'] = response.meta['image_save_fold']

            self.main_headers['referer'] = self.user_profile_url_format.format(username=img_user_info['username'])
            self.more_headers['referer'] = self.user_profile_url_format.format(username=img_user_info['username'])
            # self.more_headers['x-instagram-gis'] = hashlib.md5('guayaquil-ecuador'+str(int(time.time())).encode('utf-8')).hexdigest()

            if img_count > self.image_num_limit:
                for img in img_list:
                    if img['node']['__typename'] != 'GraphVideo':
                        item['img_id'] = img['node']['id']
                        item['img_owner_id'] = img_user_info['id']
                        item['img_owner_name'] = img_user_info['username']
                        item['img_url'] = img['node']['thumbnail_src']
                        # item['img_data'] = json.dumps(img_dict)
                        self.user_im_sum += 1
                        yield Request(item['img_url'],
                                      callback=self.get_img_content,
                                      meta={'item':item},
                                      headers=self.main_headers,
                                      errback=self.report_error)

                # time.sleep(4)

                has_next_page = img_user_info['edge_owner_to_timeline_media']['page_info']['has_next_page']
                end_cursor = img_user_info['edge_owner_to_timeline_media']['page_info']['end_cursor']
                if has_next_page:
                    url = self.more_img_format.format(query_hash=self.query_hash,
                                                      user_id=item['img_owner_id'],
                                                      end_cursor=end_cursor
                                                      )
                    yield Request(url,
                                  callback=self.parse_more_page,
                                  headers=self.more_headers,
                                  meta={'owner_id': item['img_owner_id'],
                                        'owner_name': item['img_owner_name'],
                                        'img_count': img_count,
                                        'img_save_fold': item['img_save_fold']
                                        # 'cookiejar': random.choice(self.cookie_list)
                                        },
                                  errback=self.report_error
                                  )
            else:
                self.log('*********** finish user:%s  for <limit count***********' % (item['img_owner_id']))
                set_crawled(item['img_owner_id'], int(img_count), int(time.time()))

    def parse_more_page(self, response):
        item = ImageItem()
        img_data = json.loads(response.body)
        img_list = img_data['data']['user']['edge_owner_to_timeline_media']['edges']
        img_count = img_data['data']['user']['edge_owner_to_timeline_media']['count']

        # time.sleep(100)  # test

        for img in img_list:
            if img['node']['__typename'] != 'GraphVideo':
                item['img_id'] = img['node']['id']
                item['img_owner_id'] = response.meta['owner_id']
                item['img_owner_name'] = response.meta['owner_name']
                item['img_url'] = img['node']['thumbnail_src']
                item['img_save_fold'] = response.meta['img_save_fold']
                # item['img_data'] = json.dumps(img_data)
                self.user_im_sum += 1
                yield Request(item['img_url'],
                              callback=self.get_img_content,
                              meta={'item': item,
                                    },
                              headers=self.main_headers,
                              errback=self.report_error
                              )

        has_next_page = img_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        end_cursor = img_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        if self.user_im_sum < self.image_num_limit:
            if has_next_page:
                url = self.more_img_format.format(query_hash=self.query_hash,
                                                  user_id=item['img_owner_id'],
                                                  end_cursor=end_cursor
                                                  )
                # response.meta['cookiejar'] = random.choice(self.cookie_list)
                yield Request(url,
                              callback=self.parse_more_page,
                              headers=self.more_headers,
                              meta=response.meta,
                              errback=self.report_error
                              )
                time.sleep(1)

            else:
                self.log('*********** finish user:%s ***********' % (response.meta['owner_id']))
                set_crawled(item['img_owner_id'], response.meta['img_count'], int(time.time()))
        else:
            self.log('*********** finish user:%s ***********' % (response.meta['owner_id']))
            set_crawled(item['img_owner_id'], self.image_num_limit, int(time.time()))

    def get_img_content(self, response):
        item = response.meta['item']
        item['img_content'] = response.body
        # item['img_save_fold'] = self.image_save_fold
        yield item

    def report_error(self, failure):
        if failure.value.response.status != 404 and failure.value.response.status != 500:
            utils.send_mail(self.name+'__'+socket.gethostname() + '__' + repr(failure.value.response), self.name, 'jason',
                        'crawl_exception')
        # print(failure.value.response.status,type(failure.value.response.status),failure.value.response)
        # if failure.value.response.status == 429:
        #     time.sleep(100)
