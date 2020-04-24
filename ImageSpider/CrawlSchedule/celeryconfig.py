from datetime import timedelta
from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1:6379/1' # 使用RabbitMQ作为消息代理

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1' # 把任务结果存在了Redis

CELERY_TASK_SERIALIZER = 'msgpack' # 任务序列化和反序列化使用msgpack方案

CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_ACCEPT_CONTENT = ['json', 'msgpack'] # 指定接受的内容类型
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {

    # 'product_city_url': {
    #     'task': 'CrawlSchedule.instagram_tasks.product_city_url',
    #
    #     'schedule': crontab(minute='*/30'),
    #
    #     'args': (1,'United Arab Emirates') # limt_num crawl loc
    #
    # },
    'product_loc_url':{
        'task': 'CrawlSchedule.instagram_tasks.product_loc_url',

        'schedule': crontab(minute='*/2',hour='1-7,9-18,20-23'),

        'args': (2,'Kenya') # limt_num crawl user
    },
    'product_user_url':{
        'task': 'CrawlSchedule.instagram_tasks.product_user_url',

        'schedule': crontab(minute='*/3', hour='1-7,9-18,20-23'),
        'args': (20,'Kenya') # limt_num

    },
    # 'get_yipei_number':{
    #     'task': 'CrawlSchedule.instagram_tasks.get_yipei_number',
    #
    #     'schedule': crontab(minute='*/3'),
    #     'args': (1,) # limt_num
    #
    # }
#     'product_hoc_car_url':{
#         'task': 'CrawlSchedule.instagram_tasks.product_hoc_car_url',
#
#         'schedule': crontab(minute='*'),
#         'args': (2,) # limt_num
#
#     },
#     'set_car_iscrawled_to0':{
#         'task': 'CrawlSchedule.instagram_tasks.set_car_iscrawled_to0',
#
#         'schedule': crontab(hour=23, day_of_week=0),
#         # 'args': (2,) # limt_num
#
#     }
}