from telebot.types import Message

from adagio import bot

def ping_handler(message: Message):
    bot.reply_to(message, 'pong')
    