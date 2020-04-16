# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityTagItem(scrapy.Item):
    # define the fields for your item here like:
    loc_city_name = scrapy.Field()
    loc_city_id = scrapy.Field()
    loc_parent_name = scrapy.Field()
    loc_parent_id = scrapy.Field()
    city_country_name = scrapy.Field()
    is_crawled = scrapy.Field()


class LocTagItem(scrapy.Item):
    # define the fields for your item here like:
    loc_tag_name = scrapy.Field()
    loc_id = scrapy.Field()
    loc_parent_name = scrapy.Field()
    loc_parent_id = scrapy.Field()
    loc_country_name = scrapy.Field()
    is_crawled = scrapy.Field()


class ImgUserItem(scrapy.Item):
    img_user_id = scrapy.Field()
    img_user_name = scrapy.Field()
    # full_name = scrapy.Field()
    user_profile_url = scrapy.Field()
    user_country_name = scrapy.Field()
    is_crawled = scrapy.Field()


class ImageItem(scrapy.Item):
    img_id = scrapy.Field()
    img_content = scrapy.Field()
    img_owner_id = scrapy.Field()
    img_owner_name = scrapy.Field()
    img_url = scrapy.Field()
    img_data = scrapy.Field()
    img_save_fold = scrapy.Field()


class InsTagItem(scrapy.Item):
    img_id = scrapy.Field()
    img_content = scrapy.Field()
    tag_id = scrapy.Field()
    tag_name = scrapy.Field()
    img_url = scrapy.Field()
    img_data = scrapy.Field()


class GoogleImItem(scrapy.Item):
    img_id = scrapy.Field()
    img_url = scrapy.Field()
    img_content = scrapy.Field()
    img_lable = scrapy.Field()


class CarImEntranceItem(scrapy.Item):
    entran_im_url = scrapy.Field()
    entran_brand = scrapy.Field()
    entran_series = scrapy.Field()
    entran_series_id = scrapy.Field()
    entran_main_url = scrapy.Field()
    # entran_price_url = scrapy.Field()
    # entran_forum_url = scrapy.Field()
    # entran_appraisal_url = scrapy.Field()


class CarPicItem(scrapy.Item):
     car_model = scrapy.Field()
     pic_id = scrapy.Field()
     pic_content = scrapy.Field()


class YiPeiItem(scrapy.Item):
    # car_brand = scrapy.Field()
    # car_series = scrapy.Field()
    # car_made_date = scrapy.Field()
    car_vin = scrapy.Field()
    car_vin_alias = scrapy.Field()
    car_data = scrapy.Field()
    is_crawled = scrapy.Field()

