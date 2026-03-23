import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('smart_job_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'recompute-analytics-daily': {
        'task': 'analytics.tasks.recompute_all_user_analytics',
        'schedule': crontab(hour=1, minute=0),
    },
}
