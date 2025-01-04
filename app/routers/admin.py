from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.filters import and_f
from aiogram.types.input_file import FSInputFile
from aiogram.types import File
from pony.orm import db_session, select

from ..settings import CONFIG_PATH, DB_PATH
from ..database.models import User

import yaml
import asyncio
import os

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
        users = select(u.id for u in User)[:]

    alert = await message.answer("sending...")

    counter = 0
    for u in users:
        if u == message.from_user.id:
            continue

        try:
            await message.bot.copy_message(
                chat_id=u,
                from_chat_id=message.from_user.id,
                message_id=message.reply_to_message.message_id,
            )
            counter += 1
        except:
            pass

        await asyncio.sleep(0.2)

    await alert.delete()
    await message.reply(f"sent for {counter} users")



@router.message(and_f(Command("backup"), F.from_user.id.in_(config.get('bot').get('admins', []))))
async def backup_db(message: Message) -> None:
    try:
        await message.bot.send_document(
            chat_id=message.from_user.id,
            document=FSInputFile(path=DB_PATH)
        )
    except Exception as e:
        print(e)
        await message.answer("failed to send backup")


@router.message(and_f(Command("restore"), F.from_user.id.in_(config.get('bot').get('admins', []))))
async def restore_db(message: Message) -> None:
    if not message.reply_to_message:
        await message.answer("please reply on db")
        return

    if not message.reply_to_message.document:
        await message.answer("you must reply on a document")
        return

    try:
        file_id = message.reply_to_message.document.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        await message.bot.download_file(file_path, DB_PATH)
        await message.answer("done\nrestart required!")
    except Exception as e:
        print(e)
        await message.answer("failed to restore backup")