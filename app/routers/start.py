from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

router = Router()

@router.message(Command("start"))
async def ping(message: Message) -> None:
    await message.reply("""
لطفا لینک (یوتیوب | اسپاتیفای |‌ ساوندکلاود) رو ارسال کن تا فایل صوتی‌اش رو برات ارسال کنم
""")