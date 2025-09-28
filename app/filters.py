from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message

from adagio import SUDO
from app.models import User

import re


class IsAdmin(SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: Message):
        if not message.from_user:
            return False

        user_id = message.from_user.id

        if user_id == SUDO:
            return True
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False
        
        return user.is_admin


class IsCommand(SimpleCustomFilter):
    key = 'is_command'

    @staticmethod
    def check(message: Message):
        command_pattern = r'^\/.*$'

        if not message.text:
            return False

        if re.fullmatch(command_pattern, message.text):
            return True
        
        return False


class IsText(SimpleCustomFilter):
    key = 'is_text'

    @staticmethod
    def check(message: Message):
        if not message.text:
            return False
        
        return True