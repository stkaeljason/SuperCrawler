#coding:utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import redis
import pymongo

from ImageSpider import utils

#python
from contextlib import contextmanager



conf = configparser.ConfigParser()
# ./config.stage.conf

if utils.is_dev() is True:
	conf.read('./config.stage.conf')
else:
	conf.read('./config.conf')

# mysql
mysql_host = conf['MYSQL']['mysql_host']
mysql_user = conf['MYSQL']['mysql_user']
# mysql_pwd = conf['MYSQL']['mysql_pwd']
mysql_pwd = 'jason#333#abc'
mysql_db = conf['MYSQL']['mysql_db']
mysql_port = conf['MYSQL']['mysql_port']

# redis
redis_host = conf['REDIS']['redis_host']
redis_port = conf['REDIS']['redis_port']
# redis_auth = conf['REDIS']['']

# mongo_db
mongo_host = conf['MONGODB']['mongo_host']
mongo_port = conf['MONGODB']['mongo_port']
mg_db_name = conf['MONGODB']['mg_db_name']
mg_table_name = conf['MONGODB']['mg_table_name']
# img_save
img_path = conf['IMG_SAVE_PATH']['img_path']

# path add
# add_path = conf['ADD_PATH']['add_path']

pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
redis_hander = redis.Redis(connection_pool=pool)

#proxy_port
proxy_port = conf['PROXY_PROT']['proxy_prot']


engine = create_engine('mysql+pymysql://' + mysql_user + ':' + mysql_pwd + '@' + mysql_host + ':' + mysql_port + '/' + mysql_db + '',
					   echo=False,pool_recycle=21600,pool_size=20)
DBSession = sessionmaker(bind=engine)


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
