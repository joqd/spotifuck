from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.filters import and_f
from pony.orm import db_session, select

from ..settings import CONFIG_PATH
from ..database.models import User

import yaml
import asyncio

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)


router = Router()

@router.message(and_f(Command("status"), F.from_user.id.in_(config.get('bot').get('admins', []))))
async def status(message: Message) -> None:
    with db_session:
        users = select(u.id  for u in User)[:]
    
    await message.reply(f"users: {len(users)}")



@router.message(and_f(Command("send"), F.from_user.id.in_(config.get('bot').get('admins', []))))
async def send(message: Message) -> None:
    if not message.reply_to_message:
        await message.reply("reply on a message")
        return

    with db_session:
        users = select(u.id  for u in User)[:]

    counter = 0
    for u in users:
        try:
            await message.bot.copy_message(
                chat_id=u.id,
                from_chat_id=message.from_user.id,
                message_id=message.reply_to_message.message_id,
            )
            counter += 1
        except:
            pass

        await asyncio.sleep(0.2)

    await message.reply(f"sent for {counter} users")