from settings import bot
from app.views.ping import ping_handler
from app.middlewares import WatchdogMiddleware
from app.filters import IsAdmin, IsCommand


# filters
bot.add_custom_filter(IsAdmin())
bot.add_custom_filter(IsCommand())

# middlewares
bot.setup_middleware(WatchdogMiddleware())

# handlers
bot.register_message_handler(ping_handler, commands=['ping'])