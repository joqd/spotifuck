from adagio import bot
from app.views.ping import ping_handler
from app.views.start import start_handler
from app.views.admin import status_handler, echo_handler
from app.views.spotdl_query import spotdl_query_handler
from app.middlewares import WatchdogMiddleware
from app.filters import IsAdmin, IsCommand, IsText


# filters
bot.add_custom_filter(IsAdmin())
bot.add_custom_filter(IsCommand())
bot.add_custom_filter(IsText())

# middlewares
bot.setup_middleware(WatchdogMiddleware())

# handlers
bot.register_message_handler(ping_handler, commands=['ping'])
bot.register_message_handler(start_handler, commands=['start', 'restart'])
bot.register_message_handler(status_handler, commands=['status'], is_admin=True)
bot.register_message_handler(echo_handler, commands=['echo'], is_admin=True)
bot.register_message_handler(spotdl_query_handler, is_command=False, is_text=True)