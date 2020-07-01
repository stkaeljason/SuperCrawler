from sqlalchemy import Column, String , Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

# from ImageSpider.db import add_path
# import sys
# sys.path.append(add_path)

from ImageSpider.db import DBSession
from ImageSpider import utils
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://'+'root'+':'+'jason#333#abc'+'@'+'127.0.0.1'+':'+'3306'+'/'+'img_crawler'+'')


Base = declarative_base()




class CrawlConfig(Base):
    # 表的名字:
    __tablename__ = 'crawl_config'
    id = Column(Integer, primary_key=True,autoincrement=True)
    config_name = Column(String(30),nullable=False)
    config_value = Column(String(30), nullable=False)
    config_lable = Column(String(30), nullable=True)
    # pass_wd = Column(String(20),nullable=True)
    # crawl_id = Column(String(20),nullable=True)
    # lable = Column(String(20),nullable=True)


def get_config(config_name, config_lable):
    session = DBSession()
    config_object = None
    try:
        config_object = session.query(CrawlConfig).filter(and_(CrawlConfig.config_name == config_name, CrawlConfig.config_lable == config_lable)).first()
    except Exception as e:
        print(str(e))
        utils.send_mail(str(e), 'db_session_query_CrawlConfig',
                        'jason',
                        'crawl_exception')
    finally:
        session.close()
        pass
    return config_object.config_value

# Base.metadata.create_all(bind=engine)