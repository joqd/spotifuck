from telebot import apihelper
import telebot
import environ

from pathlib import Path


env = environ.Env()
env.read_env('.env')

BOT_TOKEN: str = str(env('BOT_TOKEN'))

SUDO: int = int(env('SUDO', default=0)) # type: ignore

LOCAL_BOT_API_BASE_URL: str = env('LOCAL_BOT_API_BASE_URL', default='') # type: ignore

if LOCAL_BOT_API_BASE_URL:
    if LOCAL_BOT_API_BASE_URL.endswith('/'):
        apihelper.API_URL = LOCAL_BOT_API_BASE_URL + 'bot{0}/{1}'
    else:
        apihelper.API_URL = LOCAL_BOT_API_BASE_URL + '/bot{0}/{1}'

bot = telebot.TeleBot(
    token=BOT_TOKEN,
    use_class_middlewares=True,
    skip_pending=True,
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_HOST: str = str(env('REDIS_HOST', default='localhost')) # type: ignore

REDIS_PORT: int = int(env('REDIS_PORT', default=6379)) # type: ignore

REDIS_BROKER_DB: int = int(env('REDIS_BROKER_DB', default=0)) # type: ignore

REDIS_RESULT_DB: int = int(env('REDIS_RESULT_DB', default=1)) # type: ignore

PROXY: str | None = env('PROXY', default=None)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / 'db.sqlite3',
    }
}

SPOTIFY_CLIENT_ID: str = str(env('SPOTIFY_CLIENT_ID'))

SPOTIFY_CLIENT_SECRET: str = str(env('SPOTIFY_CLIENT_SECRET'))

COOKIE_FILE = BASE_DIR / 'cookies.txt'

DOWNLOAD_DIR = BASE_DIR / 'downloads'
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_CHANNEL: int = int(env('HISTORY_CHANNEL')) # type: ignore

TIME_ZONE = 'Asia/Tehran'


INSTALLED_APPS = ('app',)

# Celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False
CELERY_BROKER_URL    = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BROKER_DB}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULT_DB}'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_TIME_LIMIT = 60 * 2
CELERY_TASK_SOFT_TIME_LIMIT = 60 * 2
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_QUEUES = None