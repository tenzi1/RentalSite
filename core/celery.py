from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "save-messages-every-minute": {
        "task": "rentals.tasks.save_messages_from_redis",
        "schedule": 10.0,
    },
    "celery-backend-cleanup": {
        "task": "celery.backend_cleanup",
        "schedule": crontab(minute="*/1"),
    },
}
