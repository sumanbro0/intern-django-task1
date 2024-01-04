import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task9.settings')

app = Celery('task9')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'create-notification-every-minute': {
        'task': 'books.tasks.create_notification',
        'schedule': crontab(),  
    },
}

app.autodiscover_tasks()
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')