from sqlalchemy import Column, String , Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

# from ImageSpider.db import add_path
# import sys
# sys.path.append(add_path)

from ImageSpider.db import DBSession
from ImageSpider import utils
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://'+'root'+':'+'root'+'@'+'127.0.0.1'+':'+'3306'+'/'+'img_crawler'+'')


Base = declarative_base()

session = DBSession()

class ImgUser(Base):
    # 表的名字:
    __tablename__ = 'instagram_img_user'
    id = Column(Integer, primary_key=True,autoincrement=True)
    img_user_id = Column(String(30), unique=True)
    img_user_name = Column(String(100),nullable=False)
    full_name = Column(String(100),nullable=True)
    user_profile_url = Column(String(150),nullable=True)
    user_country_name = Column(String(50),nullable=True)
    image_counts = Column(Integer,nullable=True)
    crawled_time = Column(String(20),nullable=True)
    is_crawled = Column(Integer,nullable=False)



def get_img_user(limt_num, country):
    img_locs = []
    try:
        img_locs = session.query(ImgUser).filter(and_(ImgUser.is_crawled == 0, ImgUser.user_country_name == country)).limit(limt_num)
    except Exception as e:
        print(str(e))
        utils.send_mail(str(e), 'db_session_query_user',
                        'jason',
                        'crawl_exception')
    finally:
        # session.close()
        pass
    return img_locs

def set_crawled(user_id, image_counts, crawled_time,is_crawled=1):
    try:
        session.query(ImgUser).filter(ImgUser.img_user_id == user_id).update({ImgUser.is_crawled: is_crawled,
                                                                              ImgUser.image_counts:image_counts,
                                                                              ImgUser.crawled_time: crawled_time}
                                                                             )
        session.commit()
    except Exception as e:
        print(str(e))
        utils.send_mail(str(e), 'db_session_update_user',
                        'jason',
                        'crawl_exception')
        session.rollback()
    finally:
        # session.close()
        pass
# Base.metadata.create_all(bind=engine)