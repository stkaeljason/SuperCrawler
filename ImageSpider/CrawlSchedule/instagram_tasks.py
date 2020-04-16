#coding:utf-8
import hashlib
import time

from CrawlSchedule.app import app
from ImageSpider.db import redis_hander

# db
from ImageSpider.models.location_tag_model import get_img_loc
from ImageSpider.models.img_user_model import get_img_user
from ImageSpider.models.loc_city_model import get_citys
from ImageSpider.models.car_entrance_model import get_car_img_entrance
from ImageSpider.models.aicar_entrance import get_aicar_img_entrance

from ImageSpider.models.img_user_model import set_crawled
from ImageSpider.models.location_tag_model import loc_set_crawled
from ImageSpider.models.loc_city_model import city_set_crawled
from ImageSpider.models.car_entrance_model import hoc_set_crawled, is_crawled_to0
from ImageSpider.models.aicar_entrance import aicar_set_crawled
from ImageSpider.models.yipei_model import get_number, update_is_crawl


@app.task
def product_city_url(limt_num, country_name):
    city_list = get_citys(limt_num, country_name)
    for city in city_list:
        city_id = city.loc_city_id
        city_name = city.loc_city_name
        city_url = 'https://www.instagram.com/explore/locations/{}/{}/'.format(city_id,city_name)
        redis_hander.lpush('ins_loc:start_urls',city_url)
        city_set_crawled(city_id,is_crawled=2)

@app.task
def product_loc_url(limt_num, country_name):
    loc_list = get_img_loc(limt_num, country_name)
    for loc in loc_list:
        loc_id = loc.loc_id
        loc_name = loc.loc_tag_name
        loc_url = ''
        if loc_name:
            loc_url = 'https://www.instagram.com/explore/locations/{}/{}/'.format(loc_id,loc_name)
        else:
            loc_url = 'https://www.instagram.com/explore/locations/{}'.format(loc_id)
        redis_hander.lpush('img_user:start_urls',loc_url)
        loc_set_crawled(loc_id, is_crawled=2)


@app.task
def product_user_url(limt_num, country_name):
    user_list = get_img_user(limt_num, country_name)
    for user in user_list:
        user_id = user.img_user_id
        user_name = user.img_user_name
        user_profile_url = 'https://www.instagram.com/{username}/'.format(username=user_name)
        redis_hander.lpush('ins_img:start_urls',user_profile_url)
        set_crawled(user_id,0,int(time.time()),2)

@app.task
def product_hoc_car_url(limt_num):
    car_img_entrances = get_car_img_entrance(limt_num)
    for entrance in car_img_entrances:
        entrance_id = entrance.entrance_id
        entran_im_url = entrance.entran_im_url
        redis_hander.lpush('homeofcar',entran_im_url)
        hoc_set_crawled(entrance_id,is_crawled=2)

@app.task
def product_aicar_url(limt_num):
    """爱卡汽车的定时调度任务"""
    car_img_entrances = get_aicar_img_entrance(limt_num)
    for entrance in car_img_entrances:
        entrance_id = entrance.id
        entran_im_url = entrance.entran_im_url
        redis_hander.lpush('aicar',entran_im_url)
        aicar_set_crawled(entrance_id,is_crawled=2)

@app.task
def set_car_iscrawled_to0():
    is_crawled_to0()

@app.task
def get_yipei_number(limit_num):
    car_vins = get_number(limit_num)
    def compute_md5(str_name):
        return hashlib.md5(str_name.encode('utf8')).hexdigest()

    username = '18080992294'
    password = '123456'

    for car in car_vins:
        vin = car.car_number
        token = compute_md5(compute_md5(username) + compute_md5(password) + '/?vin={}'.format(vin))
        # print('token', token, vin)
        yiepi_url = 'http://api.17vin.com:8080/?vin={}&user={}&token={}'.format(vin, username, token)
        redis_hander.lpush('yipei_site', yiepi_url)
        update_is_crawl(vin, 2)