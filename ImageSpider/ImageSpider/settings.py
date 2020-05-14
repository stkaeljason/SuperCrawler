# -*- coding: utf-8 -*-

# Scrapy settings for ImageSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from ImageSpider.db import redis_host, redis_port

BOT_NAME = 'ImageSpider'

SPIDER_MODULES = ['ImageSpider.spiders']
NEWSPIDER_MODULE = 'ImageSpider.spiders'


#scrapy-redis的配置
# 过滤器
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 调度状态持久化
SCHEDULER_PERSIST = True

# 请求调度使用优先队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# redis 使用的端口和地址
REDIS_HOST = redis_host
REDIS_PORT = redis_port

# ITEM_PIPELINES
ITEM_PIPELINES = {
    'ImageSpider.pipelines.ImagespiderPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}


#设置全局和局部并发数目
# 默认 Item 并发数：100
CONCURRENT_ITEMS = 100

# 默认 Request 并发数：16
CONCURRENT_REQUESTS = 1

# 默认每个域名的并发数：8
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# 每个IP的最大并发数：0表示忽略
CONCURRENT_REQUESTS_PER_IP = 0


DOWNLOAD_DELAY = 2.0

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ImageSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 禁止重定向
# REDIRECT_ENABLED = False

#缓存设置
# 打开缓存
HTTPCACHE_ENABLED = False

# 设置缓存过期时间（单位：秒）
#HTTPCACHE_EXPIRATION_SECS = 0

# 缓存路径(默认为：.scrapy/httpcache)
HTTPCACHE_DIR = 'httpcache'

# 忽略的状态码
HTTPCACHE_IGNORE_HTTP_CODES = []

# 缓存模式(文件缓存)
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


DOWNLOADER_MIDDLEWARES = {
   'ImageSpider.middlewares.ImagespiderDownloaderMiddleware': 543,
   'ImageSpider.middlewares.ImagespiderRetryMiddleware':544,
   'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
}

RETRY_HTTP_CODES = [500, 503, 504, 400, 408,429]
RETRY_TIMES = 0

EXTENSIONS = {
   'ImageSpider.extensions.SpiderOpenEx': None,
}

# IMAGE_NUM_LIMIT = 400
TAG_IMAGE_NUM_LIMIT = 40000

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False
# COOKIES_DEBUG = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16



# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ImageSpider.middlewares.ImagespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html


# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html


# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
