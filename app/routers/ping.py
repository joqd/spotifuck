from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

router = Router()

@router.message(Command("ping"))
async def ping(message: Message) -> None:
    await message.reply("pong")