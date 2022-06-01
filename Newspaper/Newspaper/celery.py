import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Newspaper.settings')
 
app = Celery('Newspaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.conf.beat_schedule = {
    'weekly_mail': {
        'task': 'NewsPortal.tasks.send_weekly_mail',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

app.autodiscover_tasks()