# coding: utf8

from sqlalchemy import Column, String , Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

# from ImageSpider.db import add_path
# import sys
# sys.path.append(add_path)

from ImageSpider.db import DBSession
from ImageSpider import utils

from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://'+'root'+':'+'jason#333#abc'+'@'+'127.0.0.1'+':'+'3306'+'/'+'img_crawler'+'')

Base = declarative_base()

session = DBSession()

class ImgLocTag(Base):
    # 表的名字:
    __tablename__ = 'instagram_loc_tag'
    id = Column(Integer, primary_key=True,autoincrement=True)
    loc_id = Column(String(30), unique=True)
    loc_tag_name = Column(String(100),nullable=False)
    loc_parent_id = Column(String(30),nullable = True)
    loc_parent_name = Column(String(100),nullable = True)
    loc_country_name = Column(String(50),nullable = True)
    is_crawled = Column(Integer, nullable=False)



def get_img_loc(limt_num, country):
    img_locs = []
    try:
        img_locs = session.query(ImgLocTag).filter(and_(ImgLocTag.is_crawled == 0, ImgLocTag.loc_country_name == country)).limit(limt_num)
    except Exception as e:
        print(str(e))
        utils.send_mail(str(e), 'db_session_query_loc',
                        'jason',
                        'crawl_exception')
    finally:
        # session.close()
        pass
    return img_locs

def loc_set_crawled(loc_id, is_crawled):
    try:
        session.query(ImgLocTag).filter(ImgLocTag.loc_id == loc_id).update({ImgLocTag.is_crawled: is_crawled})
        session.commit()
    except Exception as e:
        print(str(e))
        utils.send_mail(str(e), 'db_session_update_loc',
                        'jason',
                        'crawl_exception')
        session.rollback()
    finally:
        # session.close()
        pass


Base.metadata.create_all(bind=engine)