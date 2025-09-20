from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message

from settings import SUDO
from app.models import User


class IsAdmin(SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: Message):
        user_id = message.from_user.id
        if user_id == SUDO:
            return True
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False
        
        return user.is_admin
