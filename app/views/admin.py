from telebot.types import Message
from django.utils import timezone

from adagio import bot
from app.models import User, Download

from datetime import timedelta


def status_handler(message: Message):
    users_count = User.objects.count()
    downloads_count = Download.objects.count()

    last_month = timezone.now() - timedelta(days=30)

    recent_users_count = User.objects.filter(created_at__gte=last_month).count()
    recent_downloads_count = Download.objects.filter(created_at__gte=last_month).count()

    template = f"""
👤 {users_count} (+`{round(recent_users_count / users_count, 2) * 100 if users_count else 0}`%)
📥 {downloads_count} (+`{round(recent_downloads_count / downloads_count, 2) * 100 if downloads_count else 0}`%)
    """

    bot.reply_to(message, template, parse_mode='markdown')