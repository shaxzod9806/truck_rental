import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motochas.settings')
app = Celery('motochas')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# celery beat tasks
app.conf.beat_schedule = {
     'move_next_renter':{
         'task': 'orders.tasks.move_renter',
         'schedule': crontab(minute='*/1')
     }
 }
# celery -A motochas worker
# celery -A motochas beat