
custom_settings_for_homeofcar = {
    'CONCURRENT_REQUESTS': 3,
    'CONCURRENT_REQUESTS_PER_DOMAIN':2,
    'CONCURRENT_REQUESTS_PER_IP':0,
    'DOWNLOAD_DELAY':0.15,
    'RETRY_TIMES':1,
    'DOWNLOADER_MIDDLEWARES': {
        'ImageSpider.middlewares.HomeOfCarDownloaderMiddleware': 543,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware':544
    },
    'ITEM_PIPELINES': {
        'ImageSpider.pipelines.HomeOfCarPipeline': 300,
    },
}

custom_settings_for_google = {
    'CONCURRENT_REQUESTS': 3,
    'CONCURRENT_REQUESTS_PER_DOMAIN':2,
    'CONCURRENT_REQUESTS_PER_IP':0,
    'DOWNLOAD_DELAY':0.15,
    'RETRY_TIMES':0,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'ImageSpider.middlewares.HomeOfCarDownloaderMiddleware': 543,
    #     'scrapy.downloadermiddlewares.retry.RetryMiddleware':544
    # },
    # 'ITEM_PIPELINES': {
    #     'ImageSpider.pipelines.HomeOfCarPipeline': 300,
    # },
}

custom_settings_for_aicar = {
    'CONCURRENT_REQUESTS': 2,
    'CONCURRENT_REQUESTS_PER_DOMAIN':2,
    'CONCURRENT_REQUESTS_PER_IP':0,
    'DOWNLOAD_DELAY':0.15,
    'RETRY_TIMES':1,
    'DOWNLOADER_MIDDLEWARES': {
        'ImageSpider.middlewares.AiCarDownloaderMiddleware': 543,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware':544
    },
    'ITEM_PIPELINES': {
        'ImageSpider.pipelines.AiCarPipeline': 300,
    },
}

custom_settings_for_yipeisite = {
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN':1,
    'CONCURRENT_REQUESTS_PER_IP':0,
    'DOWNLOAD_DELAY':0.1,
    'RETRY_TIMES':1,
    'REDIRECT_ENABLED' : False,
    'DOWNLOADER_MIDDLEWARES': {
        'ImageSpider.middlewares.YiPeiDownloaderMiddleware': 543,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware':544
    },
    'ITEM_PIPELINES': {
        'ImageSpider.pipelines.YiPeiPipeline': 300,
    },
}