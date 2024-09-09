from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Задаем настройки Django для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_auth.settings')

app = Celery('user_auth')

# Загружаем настройки из Django в celery
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(broker_connection_retry_on_startup=True)
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
# Автоматически находит задачи в приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')