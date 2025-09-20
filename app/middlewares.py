from telebot.handler_backends import BaseMiddleware

from app.models import User


class WatchdogMiddleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ['message', 'callback_query']

    def pre_process(self, message, data):
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username

        User.objects.update_or_create(
            id=user_id,
            defaults={
                'first_name': first_name,
                'username': username
            }
        )

    def post_process(self, message, data, exception=None):
        pass