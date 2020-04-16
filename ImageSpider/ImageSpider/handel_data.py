#coding:utf-8
import sys, os
sys.path.append("/data/ImageCrawlPro/ImageCrawler/ImageSpider")
from sqlalchemy import Column, String , Integer
from sqlalchemy.ext.declarative import declarative_base
# from ImageSpider.ImageSpider.db import DBSession, session_scope
# from ImageSpider.ImageSpider.models.yipei_model import YiPei

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import redis
import pymongo

#python
from contextlib import contextmanager



@contextmanager
def session_scope(Session, email_topic):
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        # utils.send_mail(str(e), email_topic,
		# 				'jason',
		# 				'crawl_exception')
        raise
    finally:
        session.close()

conf = configparser.ConfigParser()
# ./config.stage.conf
def is_dev():
	return True if os.getenv('img_crawl_env') == 'dev' else False

if is_dev() is True:
	conf.read('./config.stage.conf')
else:
	conf.read('./config.conf')

# mysql
mysql_host = conf['MYSQL']['mysql_host']
mysql_user = conf['MYSQL']['mysql_user']
mysql_pwd = conf['MYSQL']['mysql_pwd']
mysql_db = conf['MYSQL']['mysql_db']
mysql_port = conf['MYSQL']['mysql_port']
Base = declarative_base()

import getpass
if getpass.getuser() == 'ceiec':
	img_path = conf['FACE02']['img_path']
elif getpass.getuser() == 'ubuntu':
	img_path = conf['UBUNTU']['img_path']
else:
	img_path = conf['IMG_SAVE_PATH']['img_path']

engine = create_engine('mysql+pymysql://' + mysql_user + ':' + mysql_pwd + '@' + mysql_host + ':' + mysql_port + '/' + mysql_db + '',
					   echo=False,pool_recycle=21600,pool_size=20)
DBSession = sessionmaker(bind=engine)

class YiPei(Base):
    # 表的名字:
    __tablename__ = 'yipeiwang'
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    id = Column(Integer, primary_key=True,autoincrement=True)
    car_brand = Column(String(45),nullable=True)
    car_series = Column(String(45),nullable=True)
    car_made_date = Column(String(45),nullable=True)
    car_number = Column(String(45),nullable=True,unique=True)
    is_crawled = Column(Integer)

def insert_mysql_one():
    file_path = sys.argv[1]
    # session = DBSession()
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            data_list = line.split(',')
            car_num = data_list[14]
            if car_num:
                yipei = YiPei(car_number=car_num, is_crawled=0)
                session = DBSession()
                try:
                    session.add(yipei)
                    session.commit()
                except Exception as e:
                    print(str(e))
                    session.rollback()
                finally:
                    session.close()
                print(car_num, i)


def insert_mysql_two():
    import csv
    # import pandas as pd
    file_path = sys.argv[1]
    # session = DBSession()
    with open(file_path) as csf_f:
    # ws_data = pd.read_csv(file_path, encoding='gbk')
        reader = csv.reader(csf_f)

    # read = csv.reader(csf_f)
        for index, line in enumerate(reader):
            print(line)
            data_list = line.split(',')
            car_num = data_list[2]
            if car_num:
                yipei = YiPei(car_number=car_num, is_crawled=0)
                session = DBSession()
                try:
                    session.add(yipei)
                    session.commit()
                except Exception as e:
                    print(str(e))
                    session.rollback()
                finally:
                    session.close()
                print(car_num, index)


def crawl_bran_vin():
    import hashlib
    import csv
    import sys
    import requests
    import json
    import time

    def compute_md5(str_name):
        return hashlib.md5(str_name.encode('utf8')).hexdigest()


    csv_file = sys.argv[1]
    username = '18080992294'
    password = '123456'
    car_dict = dict()
    with open(csv_file, "r", encoding="utf-8") as csf_f:
        read = csv.reader(csf_f)
        for index, line in enumerate(read[:10001]):
            vin = line[1]  # modify base the real csv
            token = compute_md5(compute_md5(username) + compute_md5(password) + '/?vin={}'.format(vin))
            print('token', token, vin, index)
            url = 'http://api.17vin.com:8080/?vin={}&user={}&token={}'.format(vin, username, token)
            for i in range(3):
                res = requests.get(url)
                if res.status_code == 200:
                    break
            result = res.json()
            if result['code'] != 1:
                print("request fail")
                break
            data = result['data']['model_list'][0]
            car_dict['vin_alias'] = vin[0:8]
            car_dict['vin'] = vin
            # car_dict['brand'] = result['Brand']
            # car_dict['brand_en'] = result['Brand_en']
            # car_dict['series'] = result['Series']
            # car_dict['series_en'] = result['Series_en']
            # car_dict['model_year'] = result['Model_year']
            # car_dict['model_detail'] = result['Model_detail']
            car_dict['data'] = data
            vin_file = os.path.join(img_path, 'vin_brand.json')
            with open(vin_file, 'a') as f:
                f.write(json.dumps(car_dict, ensure_ascii=False) + '\n')
            time.sleep(2)
        else:
            print('break break:%s'%index)
        print('collect done')


if __name__ == "__main__":
    crawl_bran_vin()
