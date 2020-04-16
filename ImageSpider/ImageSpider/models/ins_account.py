from sqlalchemy import Column, String , Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

# from ImageSpider.db import add_path
# import sys
# sys.path.append(add_path)

from ImageSpider.db import DBSession
from ImageSpider import utils
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://'+'root'+':'+'root'+'@'+'127.0.0.1'+':'+'3306'+'/'+'img_crawler'+'')


Base = declarative_base()

session = DBSession()


class InsUser(Base):
    # 表的名字:
    __tablename__ = 'ins_account'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_name = Column(String(50),nullable=False)
    pass_wd = Column(String(20),nullable=True)
    crawl_id = Column(String(20),nullable=True)
    lable = Column(String(20),nullable=True)


def get_ins_user(crawl_id):
    ins_user = []
    try:
        ins_user = session.query(InsUser).filter(InsUser.crawl_id == crawl_id)
    except Exception as e:
        print(str(e))
        utils.send_mail(str(e), 'db_session_query_InsUser',
                        'jason',
                        'crawl_exception')
    finally:
        # session.close()
        pass
    return ins_user

Base.metadata.create_all(bind=engine)