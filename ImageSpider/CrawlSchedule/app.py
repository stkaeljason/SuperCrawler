from __future__ import absolute_import

from celery import Celery

app = Celery('CrawlSchedule', include=['CrawlSchedule.instagram_tasks'])

app.config_from_object('CrawlSchedule.celeryconfig')


if __name__ == '__main__':

    app.start()