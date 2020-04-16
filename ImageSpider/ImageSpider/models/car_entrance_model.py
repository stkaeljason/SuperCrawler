# coding: utf8

from sqlalchemy import Column, String , Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

# from ImageSpider.db import add_path
# import sys
# sys.path.append('/home/jason/ceiec_project/ImageCrawl/ImageSpider')

from ImageSpider.db import DBSession
from ImageSpider import utils

from ImageSpider.db import session_scope

# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://'+'root'+':'+'root'+'@'+'127.0.0.1'+':'+'3306'+'/'+'img_crawler'+'')

Base = declarative_base()

# session = DBSession()


class CarEntrance(Base):
    # 表的名字:
    __tablename__ = 'hoc_image_entrances'
    entrance_id = Column(Integer, primary_key=True, autoincrement=True)
    entran_im_url = Column(String(100), unique=True, nullable=False)
    entran_brand = Column(String(30),nullable=False)
    entran_series = Column(String(30),nullable=False)
    entran_series_id = Column(Integer, nullable=False)
    entran_main_url = Column(String(100), nullable=True)
    is_crawled = Column(Integer, nullable=False)
    # __table_args__ = {
    #     'mysql_charset': 'utf8'
    # }


def get_car_img_entrance(limt_num):
    car_entrances = []
    with session_scope(DBSession, 'CarEntrance get_car_img_entrance') as session:
        car_entrances = session.query(CarEntrance).filter(CarEntrance.is_crawled == 0).limit(limt_num)
    return car_entrances


def hoc_set_crawled(entrance_id, is_crawled=1):
    with session_scope(DBSession, 'CarEntrance hoc_set_crawled') as session:
        session.query(CarEntrance).filter(CarEntrance.entrance_id == entrance_id).update({CarEntrance.is_crawled: is_crawled})


def hoc_setcrawled_base_series_id(series_id, is_crawled=1):
    with session_scope(DBSession, 'CarEntrance hoc_setcrawled_base_series_id') as sess:
        sess.query(CarEntrance).filter(CarEntrance.entran_series_id == series_id).update({CarEntrance.is_crawled: is_crawled})

def is_crawled_to0():
    with session_scope(DBSession, 'CarEntrance update_to0') as sess:
        sess.query(CarEntrance).update({CarEntrance.is_crawled: 0})

# Base.metadata.create_all(bind=engine)