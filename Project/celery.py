import os
from celery import Celery

# Celery Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL


# Beat Settings
# from celery.schedules import crontab
# app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'
#
# app.conf.beat_schedule = {
#     'every_day_12_am': {
#         'task': 'users.tasks.end_user_free_trial_period',
#         'schedule': crontab(hour="0", minute="0"),
#     },
#     'every_day_2_am': {
#         'task': 'core.tasks.ingest_price_data',
#         'schedule': crontab(hour="2", minute="0"),
#     },
#     'every_day_3_am': {
#         'task': 'core.tasks.data_prediction_process',
#         'schedule': crontab(hour="3", minute="0"),
#     },
# }


# Start services
""" Local env """
# celery -A Project worker -l INFO --pidfile="worker.pid"
""" Production env """
# celery -A Project worker -l INFO --pidfile="worker.pid" --logfile="/home/ubuntu/logs/worker.log" --detach