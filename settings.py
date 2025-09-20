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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS = ('app',)