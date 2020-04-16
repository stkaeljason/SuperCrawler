from sqlalchemy import Column, String , Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

from ImageSpider.db import DBSession
from ImageSpider.db import session_scope
from ImageSpider import utils
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://'+'root'+':'+'root'+'@'+'127.0.0.1'+':'+'3306'+'/'+'img_crawler'+'')


Base = declarative_base()
# session = DBSession()


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


def get_number(limt_num):
    ins_user = []
    with session_scope(DBSession, 'get_yipei_number') as session:
        ins_user = session.query(YiPei).filter(YiPei.is_crawled == 0).limit(limt_num)
    return ins_user


def update_is_crawl(car_number, code):
    with session_scope(DBSession, 'update yipei is_crawl') as session:
        session.query(YiPei).filter(YiPei.car_number == car_number).update({YiPei.is_crawled: code})