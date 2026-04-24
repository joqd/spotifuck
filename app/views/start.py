from telebot.types import Message

from spotifuck import bot

def start_handler(message: Message):
    bot.reply_to(message, '🎵 Drop a link, grab the vibes! YouTube & SoundCloud tunes, served fresh.')
    