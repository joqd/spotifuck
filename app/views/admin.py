from telebot.types import Message
from django.utils import timezone

from spotifuck import bot
from app.models import User, Download
from app.tasks import send_message_to_all_users

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


def echo_handler(message: Message):
    if not message.from_user.id:
        return

    reply_to_message = message.reply_to_message
    if not reply_to_message:
        bot.reply_to(message, 'You need to reply on a message')
        return

    args = message.text.split()
    if len(args) == 2:
        try:
            receiver_id = int(args[1])
        except:
            bot.reply_to(message, 'invalid user id')
            return

        try:
            bot.copy_message(
                chat_id=receiver_id,
                from_chat_id=message.from_user.id,
                message_id=reply_to_message.id,
            )

            return
        except:
            bot.reply_to(message, 'user block the bot')
            return
    else:
        send_message_to_all_users.delay(message.from_user.id, reply_to_message.id)

