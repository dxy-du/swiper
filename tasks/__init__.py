'''
Celery 异步任务

启动命令: celery worker -A tasks --loglevel=info
'''

import os

from celery import Celery

from tasks import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")

celery_app = Celery('async_tasks')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()
