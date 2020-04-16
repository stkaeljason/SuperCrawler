# coding: utf8

from sqlalchemy import Column, String , Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

from ImageSpider.db import DBSession
from ImageSpider.db import session_scope

# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://'+'root'+':'+'root'+'@'+'127.0.0.1'+':'+'3306'+'/'+'img_crawler'+'')

Base = declarative_base()


class AiCarEntrance(Base):
    # 表的名字:
    __tablename__ = 'aicar_image_entrances'
    id = Column(Integer, primary_key=True, autoincrement=True)
    entran_im_url = Column(String(100), unique=True, nullable=False)
    entran_brand = Column(String(30),nullable=False)
    entran_series = Column(String(30),nullable=False)
    entran_series_id = Column(String(30), nullable=False)
    is_crawled = Column(Integer, nullable=False)
    # __table_args__ = {
    #     'mysql_charset': 'utf8'
    # }


def get_aicar_img_entrance(limt_num):
    car_entrances = []
    with session_scope(DBSession, 'CarEntrance get_car_img_entrance') as session:
        car_entrances = session.query(AiCarEntrance).filter(AiCarEntrance.is_crawled == 0).limit(limt_num)
    return car_entrances


def aicar_set_crawled(entrance_id, is_crawled=1):
    with session_scope(DBSession, 'CarEntrance hoc_set_crawled') as session:
        session.query(AiCarEntrance).filter(AiCarEntrance.id == entrance_id).update({AiCarEntrance.is_crawled: is_crawled})


def aicar_setcrawled_base_series_id(series_id, is_crawled=1):
    with session_scope(DBSession, 'CarEntrance hoc_setcrawled_base_series_id') as sess:
        sess.query(AiCarEntrance).filter(AiCarEntrance.entran_series_id == series_id).update({AiCarEntrance.is_crawled: is_crawled})


def aicar_crawled_to0():
    with session_scope(DBSession, 'CarEntrance update_to0') as sess:
        sess.query(AiCarEntrance).update({AiCarEntrance.is_crawled: 0})

# Base.metadata.create_all(bind=engine)