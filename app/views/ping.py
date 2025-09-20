from telebot.types import Message

from settings import bot

def ping_handler(message: Message):
    bot.reply_to(message, 'pong')
    