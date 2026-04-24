from celery import Celery
from celery.schedules import crontab

import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spotifuck.settings")

app = Celery("spotifuck")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-every-night-at-22': {
        'task': 'app.tasks.random_nightly_music',
        'schedule': crontab(hour=13, minute=4),
    },
}