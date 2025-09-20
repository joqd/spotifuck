from settings import bot
from app.views.ping import ping_handler
from app.middlewares import WatchdogMiddleware
from app.filters import IsAdmin


# filters
bot.add_custom_filter(IsAdmin())

# middlewares
bot.setup_middleware(WatchdogMiddleware())

# handlers
bot.register_message_handler(ping_handler, commands=['ping'])