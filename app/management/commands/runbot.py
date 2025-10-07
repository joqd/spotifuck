from django.core.management import BaseCommand
from django.db import connections

from adagio import bot
from app import urls as _

from typing import Any


class Command(BaseCommand):
    help = 'Run the bot'

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            username = bot.get_me().username
            self.stdout.write(self.style.SUCCESS(f'- {username} started.'))
            bot.infinity_polling()
            self.stdout.write(self.style.SUCCESS(f'- {username} stopped.'))
        finally:
            connections.close_all()