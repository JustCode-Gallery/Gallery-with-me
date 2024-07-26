from __future__ import absolute_import 
import os
from celery import Celery # Django의 세팅 모듈을 Celery의 기본으로 사용하도록 등록합니다.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')

app = Celery('e-commerce')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'sample_task': {
        'task': 'seller.tasks.sample_task',
        'schedule': crontab(minute='*/1'),  # 매 1분마다 실행
        'args': (),
    },
}