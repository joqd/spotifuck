from telebot.types import Message
from django.utils import timezone

from spotifuck import bot
from app.models import User
from app.tasks import send_song_to_all_users

from datetime import timedelta


def tune_handler(message: Message):
    if not message.from_user:
        return

    try:
        user = User.objects.get(id=message.from_user.id)
    except User.DoesNotExist:
        return

    if not user.promoted_at:
        bot.reply_to(message, text='You are not authorized to use this command at this time 🥲')
        return

    now = timezone.now()
    ok_time = user.promoted_at + timedelta(hours=24)

    if now > ok_time:
        bot.reply_to(message, text='You are not authorized to use this command at this time 🥲')
        return

    reply_to_message = message.reply_to_message
    if not reply_to_message or not reply_to_message.audio:
        bot.reply_to(message, text='You have to replay on a song')
        return

    send_song_to_all_users.delay(
        message.from_user.id, 
        reply_to_message.id,
        message.from_user.first_name
    )

    user.promoted_at = None
    user.save()