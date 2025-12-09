from telebot.types import Message
from django.utils import timezone

from app.tasks import downloader
from app.models import User
from adagio import bot



def spotdl_query_handler(message: Message):
    if not message.from_user:
        return

    try:
        user = User.objects.get(id=message.from_user.id)
    except User.DoesNotExist:
        return

    now = timezone.now()
    if user.last_request_at:
        dif = now - user.last_request_at

        if dif.total_seconds() < float(15):
            bot.send_message(message.from_user.id, text='Slower you fucking idiot')
            return

    user.last_request_at = now
    user.save()

    n = bot.send_message(message.from_user.id, text='🙄 You are in line. please wait...')
    downloader.delay(message.text, message.from_user.id, n.id)
    