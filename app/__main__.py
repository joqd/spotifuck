from aiogram import Dispatcher, Bot

from .settings import DB_PATH, CONFIG_PATH
from .database import db, models as _
from . import middlewares
from . import routers

import logging
import asyncio
import yaml


with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)


async def main():
    dp = Dispatcher()
    bot = Bot(token=config["bot"]["token"])

    routers.setup(dp)
    middlewares.setup(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    
    db.bind(provider="sqlite", filename=DB_PATH, create_db=True)
    db.generate_mapping(create_tables=True)

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())