from __future__ import absolute_import 
import os
from celery import Celery # Django의 세팅 모듈을 Celery의 기본으로 사용하도록 등록합니다.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')

app = Celery('e-commerce')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_order_status_and_create_settlement': {
        'task': 'seller.tasks.update_order_status_and_create_settlement',
        'schedule': crontab(minute='*/10'),  # 10분마다 실행
    },
    'update_settlement_status': {
        'task': 'seller.tasks.update_settlement_status',
        'schedule': crontab(hour=12, minute=0),  # 매일 정오에 실행
    },
}