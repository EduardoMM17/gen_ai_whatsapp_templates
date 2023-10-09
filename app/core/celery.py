from celery import Celery
from app.core.config import settings


class CeleryConfig:
    broker_url = settings.CELERY_BROKER_URL
    result_backend = settings.CELERY_RESULT_BACKEND
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    enable_utc = True


def make_celery(app_name=__name__):
    celery = Celery(app_name)
    celery.conf.update(CeleryConfig.__dict__)
    return celery


celery = make_celery()
