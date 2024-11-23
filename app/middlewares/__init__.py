from aiogram import Dispatcher

from . import (
    user_validator_middleware,
)


def setup(dp: Dispatcher):
    dp.message.middleware(user_validator_middleware.Middleware())
    dp.callback_query.middleware(user_validator_middleware.Middleware(is_callback=True))