from .celery import app as celery_app
from .settings import *

__all__ = ('celery_app',)
