from telebot.types import Message

from adagio import bot

def start_handler(message: Message):
    bot.reply_to(message, 'Hello World')
    