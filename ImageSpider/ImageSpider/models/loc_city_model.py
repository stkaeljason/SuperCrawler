# coding: utf8

from sqlalchemy import Column, String , Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from ImageSpider import utils


from ImageSpider.db import DBSession

session = DBSession()


from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://'+'root'+':'+'jason#333#abc'+'@'+'127.0.0.1'+':'+'3306'+'/'+'img_crawler'+'')

Base = declarative_base()

class LocCityTag(Base):
    # 表的名字:
    __tablename__ = 'instagram_city_tag'
    id = Column(Integer, primary_key=True,autoincrement=True)
    loc_city_id = Column(String(30), unique=True)
    loc_city_name = Column(String(100),nullable=False)
    loc_parent_id = Column(String(30),nullable = True)
    loc_parent_name = Column(String(100),nullable = True)
    city_country_name = Column(String(50),nullable = True)
    is_crawled = Column(Integer, nullable=False)



def get_citys(limt_num, country):
    citys=[]
    try:
        citys = session.query(LocCityTag).filter(and_(LocCityTag.is_crawled == 0, LocCityTag.city_country_name == country)).limit(limt_num)
    except Exception as e:
        print(str(e))
        utils.send_mail(str(e), 'db_session_query_city',
                        'jason',
                        'crawl_exception')
        # session.rollback()
    return citys


def city_set_crawled(city_id,is_crawled=1):
    try:
        session.query(LocCityTag).filter(LocCityTag.loc_city_id == city_id).update({LocCityTag.is_crawled: is_crawled})
        session.commit()
    except Exception as e:
        print(str(e))
        utils.send_mail(str(e), 'db_session_update_city',
                        'jason',
                        'crawl_exception')
        session.rollback()
    finally:
        # session.close()
        pass

Base.metadata.create_all(bind=engine)


