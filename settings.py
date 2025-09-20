from telebot import apihelper
import telebot
import environ

from pathlib import Path


env = environ.Env()
env.read_env()

BOT_TOKEN: str = str(env('BOT_TOKEN'))

LOCAL_BOT_API_BASE_URL: str = env('LOCAL_BOT_API_BASE_URL', default='') # type: ignore

if LOCAL_BOT_API_BASE_URL:
    if LOCAL_BOT_API_BASE_URL.endswith('/'):
        apihelper.API_URL = LOCAL_BOT_API_BASE_URL + 'bot{0}/{1}'
    else:
        apihelper.API_URL = LOCAL_BOT_API_BASE_URL + '/bot{0}/{1}'

bot = telebot.TeleBot(token=BOT_TOKEN, use_class_middlewares=True)

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = "6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_HOST: str = str(env('REDIS_HOST', default='localhost')) # type: ignore

REDIS_PORT: int = int(env('REDIS_PORT', default=6379)) # type: ignore

REDIS_BROKER_DB: int = int(env('REDIS_BROKER_DB', default=0)) # type: ignore

REDIS_RESULT_DB: int = int(env('REDIS_RESULT_DB', default=1)) # type: ignore

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / 'db.sqlite3',
    }
}

TIME_ZONE = 'UTC'

INSTALLED_APPS = ('app',)

# Celery
CELERY_BROKER_URL    = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BROKER_DB}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULT_DB}'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TIME_LIMIT = 30
CELERY_TASK_SOFT_TIME_LIMIT = 25
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_QUEUES = None