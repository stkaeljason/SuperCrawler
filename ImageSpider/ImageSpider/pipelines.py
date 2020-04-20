# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# item
import os
import json
import pymysql
from ImageSpider.items import LocTagItem
from ImageSpider.items import ImgUserItem
from ImageSpider.items import CityTagItem
from ImageSpider.items import ImageItem
from ImageSpider.items import GoogleImItem
from ImageSpider.items import CarImEntranceItem
from ImageSpider.items import CarPicItem
from ImageSpider.items import InsTagItem
from ImageSpider.items import YiPeiItem


# db
import pymongo
from ImageSpider.models.location_tag_model import ImgLocTag
from ImageSpider.models.img_user_model import ImgUser
from ImageSpider.models.loc_city_model import LocCityTag
from ImageSpider.models.car_entrance_model import CarEntrance
from ImageSpider.models.aicar_entrance import AiCarEntrance
from ImageSpider.models.yipei_model import YiPei
from ImageSpider.db import DBSession
from ImageSpider.db import img_path
from ImageSpider.db import session_scope

# jason
from ImageSpider import utils


class ImagespiderPipeline(object):

    def open_spider(self, spider):
        self.session = DBSession()
        self.session.execute('SET NAMES utf8;')
        self.session.execute('SET CHARACTER SET utf8;')
        self.session.execute('SET character_set_connection=utf8;')

        # client = pymongo.MongoClient('mongodb://{host}:{port}/'.format(host=mongo_host,port=mongo_port))
        # db = client[mg_db_name]
        # self.mg_table = db[mg_table_name]

    def process_item(self, item, spider):
        if isinstance(item, CityTagItem):
            city_tag = LocCityTag(
                loc_city_id= item['loc_city_id'],
                loc_city_name = item['loc_city_name'],
                loc_parent_id = item['loc_parent_id'],
                loc_parent_name = item['loc_parent_name'],
                city_country_name= item['city_country_name'],
                is_crawled = item['is_crawled'],
            )
            try:
                self.session.add(city_tag)
                self.session.commit()
            except Exception as e:
                print(str(e))
                utils.send_mail(str(e), 'ImagespiderPipeline', 'jason', 'CityTagItem_exception')
                self.session.rollback()
            return item

        elif isinstance(item, LocTagItem):
            img_loc_tag = ImgLocTag(
                loc_tag_name = item['loc_tag_name'],
                loc_id = item['loc_id'],
                loc_parent_name = item['loc_parent_name'],
                loc_parent_id = item['loc_parent_id'],
                loc_country_name = item['loc_country_name'],
                is_crawled = item['is_crawled']
            )
            try:
                self.session.add(img_loc_tag)
                self.session.commit()
            except Exception as e:
                print(str(e))
                utils.send_mail(str(e), 'ImagespiderPipeline', 'jason', 'LocTagItem_exception')
                self.session.rollback()
            return item

        elif isinstance(item, ImgUserItem):
            img_user = ImgUser(
                img_user_name = item['img_user_name'],
                img_user_id = item['img_user_id'],
                user_country_name = item['user_country_name'],
                is_crawled = item['is_crawled'],
                user_profile_url = item['user_profile_url']
            )
            try:
                self.session.add(img_user)
                self.session.commit()
            except Exception as e:
                print("Duplicate entry %s for key img_user_id" % item['img_user_id'])
                self.session.rollback()
            return item

        elif isinstance(item, ImageItem):
            # save image to file
            try:
                face_folder = item['img_owner_name']+'_'+item['img_owner_id']
                # image_fold = img_path+'image_data/'+face_folder+'/'
                image_fold = img_path + item['img_save_fold'] + '/' + face_folder + '/'
                image_name = image_fold + item['img_id'] + '.jpg'
                # print('****************'+'         '+image_name)
                if not os.path.exists(image_fold):
                    # os.mkdir(img_path+img_folder+'/')
                    os.makedirs(image_fold)
                with open(image_name, 'wb') as f:
                    f.write(item['img_content'])

                # save mongodb
                # image_dict = {'url':item['img_url'], 'all_data':item['img_data']}
                # self.mg_table.insert(image_dict)
            except Exception as e:
                utils.send_mail(str(e), 'ImagespiderPipeline', 'jason', 'ImageItem_exception')
            return item
        elif isinstance(item, GoogleImItem):
            try:
                # img_folder = item['img_name']+'_'+item['img_owner_id']
                image_cate = ''
                if item['img_url'].endswith('.png'):
                    image_cate='.png'
                else:
                    image_cate='.jpg'


                img_folder = img_path + 'google_data/'+item['img_lable'] + '/'
                image_name = img_folder + item['img_id'] + image_cate
                # print('****************'+'         '+image_name)
                if not os.path.exists(img_folder):
                    # os.mkdir(img_path+img_folder+'/')
                    os.makedirs(img_folder)
                with open(image_name, 'wb') as f:
                    f.write(item['img_content'])

                # save mongodb
                # image_dict = {'url':item['img_url'], 'all_data':item['img_data']}
                # self.mg_table.insert(image_dict)
            except Exception as e:
                utils.send_mail(str(e), 'ImagespiderPipeline', 'jason', 'ImageItem_exception')
            return item

        elif isinstance(item, InsTagItem):
            # save image to file
            try:
                face_folder = item['tag_name']
                image_fold = img_path+'instagram_data/'+face_folder+'/'
                image_name = image_fold + item['img_id'] + '.jpg'
                # print('****************'+'         '+image_name)
                if not os.path.exists(image_fold):
                    # os.mkdir(img_path+img_folder+'/')
                    os.makedirs(image_fold)
                with open(image_name, 'wb') as f:
                    f.write(item['img_content'])

                # save mongodb
                # image_dict = {'url':item['img_url'], 'all_data':item['img_data']}
                # self.mg_table.insert(image_dict)
            except Exception as e:
                utils.send_mail(str(e), 'ImagespiderPipeline', 'jason', 'ImageItem_exception')
            return item

    def close_spider(self, spider):
        self.session.close()


class HomeOfCarPipeline(object):

    def __init__(self):
        self.Session = DBSession

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, CarImEntranceItem):
            """保存汽车之家各个车型图片入口url"""
            car_entrance = CarEntrance(
                entran_im_url = item['entran_im_url'],
                entran_brand = item['entran_brand'],
                entran_series=item['entran_series'],
                entran_series_id = item['entran_series_id'],
                entran_main_url = item['entran_main_url'],
                # entran_price_url = item['entran_price_url'],
                # entran_forum_url = item['entran_forum_url'],
                # entran_appraisal_url = item['entran_appraisal_url'],
                is_crawled = 0
            )
            with session_scope(self.Session, 'insert_car_entrance') as session:
                session.add(car_entrance)
            return item

        elif isinstance(item, CarPicItem):
            """按车型保存汽车之家图片"""
            try:
                car_folder = item['car_model']
                image_fold = img_path+'homeOfcars/'+car_folder+'/'
                image_name = image_fold + item['pic_id'] + '.jpg'
                print('****************'+'         '+image_name)
                if not os.path.exists(image_fold):
                    # os.mkdir(img_path+img_folder+'/')
                    os.makedirs(image_fold)
                with open(image_name, 'wb') as f:
                    f.write(item['pic_content'])
            except Exception as e:
                utils.send_mail(str(e), 'ImagespiderPipeline', 'jason', 'CarPicItem_exception')
            return item

    def close_spider(self, spider):
        pass


class AiCarPipeline(object):

    def __init__(self):
        self.Session = DBSession

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, CarImEntranceItem):
            """保存汽车之家各个车型图片入口url"""
            car_entrance = AiCarEntrance(
                entran_im_url = item['entran_im_url'],
                entran_brand = item['entran_brand'],
                entran_series=item['entran_series'],
                entran_series_id = item['entran_series_id'],
                is_crawled = 0
            )
            with session_scope(self.Session, 'insert_car_entrance') as session:
                session.add(car_entrance)
            return item

        elif isinstance(item, CarPicItem):
            """按车型保存汽车之家图片"""
            try:
                car_folder = item['car_model']
                image_fold = img_path+'homeOfcars/'+car_folder+'/'
                image_name = image_fold + item['pic_id'] + '.jpg'
                print('****************'+'         '+image_name)
                if not os.path.exists(image_fold):
                    # os.mkdir(img_path+img_folder+'/')
                    os.makedirs(image_fold)
                with open(image_name, 'wb') as f:
                    f.write(item['pic_content'])
            except Exception as e:
                utils.send_mail(str(e), 'ImagespiderPipeline', 'jason', 'CarPicItem_exception')
            return item

    def close_spider(self, spider):
        pass


class YiPeiPipeline(object):

    def __init__(self):
        self.Session = DBSession

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, YiPeiItem):
            """save yipei data"""
            dict_data = dict(item)
            save_path = os.path.join(img_path)
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            yipei_file = os.path.join(save_path, 'vin_data.json')
            with open(yipei_file, 'a') as f:
                f.write(json.dumps(dict_data, ensure_ascii=False)+'\n')
            return item

    def close_spider(self, spider):
        pass