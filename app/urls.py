from settings import bot
from app.views.ping import ping_handler
from app.middlewares import WatchdogMiddleware


# middlewares
bot.setup_middleware(WatchdogMiddleware())

# handlers
bot.register_message_handler(ping_handler, commands=['ping'])