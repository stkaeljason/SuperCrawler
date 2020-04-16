#coding:utf-8
import json

from scrapy import signals
from scrapy.exceptions import NotConfigured
from ImageSpider.crawl_accounts import accounts

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest


class SpiderOpenEx(object):
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

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise

        # NotConfigured otherwise

        # if not crawler.settings.getbool('MYEXT_ENABLED'):
        #
        #     raise NotConfigured

        # get the number of items from settings

        # item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

        # instantiate the extension object

        ext = cls(crawler)
        # ext.name = 'test'              #
        # ext.account_list = []            #

        # connect the extension object to signals

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        #
        # crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object

        return ext

    def spider_opened(self, spider):
        spider.log("open spider %s" % spider.name)



    def spider_closed(self, spider):
        spider.log("closed spider %s" % spider.name)

    # def item_scraped(self, item, spider):
    #     self.items_scraped += 1
    #     if self.items_scraped % self.item_count == 0:
    #         spider.log("scraped %d items" % self.items_scraped)

    # def parse(self, response):
    #     login_page = 'https://www.instagram.com/'
    #     # form_data = random.choice(account_list)
    #     form_data = account_list[0]  # test
    #     print(form_data)
    #
    #     cookiejar_name = form_data['username']
    #     self.cookie_list.append(cookiejar_name)
    #     return Request(login_page,
    #                    meta={'cookiejar': cookiejar_name, 'profile_response': response, 'formdata': form_data},
    #                    callback=self.login, errback=self.report_error, dont_filter=True)
