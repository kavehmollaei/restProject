import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("modelTamrin")  # type: ignore

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
app.conf.beat_schedule = {
    "my_task_in_every_2_sec": {
        "task": "modelTamrin.tasks.my_task2",
        "schedule": 90.0,  # run every 90 seconds   
        },
    }


__all__ = ("app",)
