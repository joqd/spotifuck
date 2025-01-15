from aiogram.types import Message, FSInputFile, URLInputFile
from aiogram import Router, F
from yt_dlp import YoutubeDL

from ..settings import DOWNLOAD_DIR, COOKIE_FILE_PATH
from ..utils import cleanup_file
from ..utils import spam_checker
from .. import errors

from uuid import uuid4
import asyncio
import re
import os

router = Router()


# Constants
YOUTUBE_URL_REGEX = r".*((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?.*"
MAX_FILESIZE = 49 * (1024 * 1024)  # 49 MB
AUDIO_FORMAT = 'mp3'


@router.message(F.text.regexp(YOUTUBE_URL_REGEX))
async def youtube_url(message: Message) -> None:
    """
    Handles messages containing YouTube URLs, downloads the audio, and uploads it.
    """
    seconds = spam_checker(message.from_user.id)
    if seconds:
        await message.reply(f"برای جلوگیری از اسپم لطفا {seconds} ثانیه دیگر تلاش کنید")
        return
    
    link = re.findall(r'https?://[^\s]+', message.text)[0]
    alert = await message.answer("🔎 دریافت اطلاعات از یوتیوب")
    audio_path = None

    try:
        # Download the audio file
        audio_path, info = await download_audio(link)
        if not audio_path.endswith(f".{AUDIO_FORMAT}"):
            audio_path += f".{AUDIO_FORMAT}"
            
        await alert.edit_text("📤 در حال آپلود...")

        # Get file size in bytes
        file_size_bytes = os.path.getsize(audio_path)
        file_size_mb = file_size_bytes // (1024 * 1024)
        if file_size_mb > 49:
            raise errors.OversizeFile()

        # Send the audio file to the user
        await send_audio(message, audio_path, info)
        await alert.delete()

    except errors.OversizeFile:
        await alert.edit_text("به دلیل محدودیت های تلگرام امکان آپلود فایل های بیشتر از ۵۰ مگابایت وجود ندارد")
    except asyncio.TimeoutError:
        await alert.edit_text("مهلت انجام عملیات به پایان رسید، لطفا دوباره تلاش کنید")
    except errors.IsLive:
        await alert.edit_text("امکان دانلود صوت ویدیو های لایو وجود ندارد")
    except Exception as e:
        print(f"Unexpected error: {e}")
        await alert.edit_text("یک خطای غیر منتظره رخ داد، لطفا بعدا تلاش کنید")
    finally:
        if audio_path:
            cleanup_file(audio_path)


async def download_audio(url: str) -> tuple[str, dict]:
    """
    Downloads the audio from the given YouTube URL and returns the file path and metadata.
    """
    outtmpl = (DOWNLOAD_DIR / f'{str(uuid4())}').as_posix()
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': AUDIO_FORMAT,
        }],
        'max_filesize': MAX_FILESIZE,
        'outtmpl': outtmpl,
        'noplaylist': True,
    }

    if os.path.exists(COOKIE_FILE_PATH):
        ydl_opts['cookiefile'] = COOKIE_FILE_PATH

    def inner():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info = ydl.sanitize_info(info)

            if info.get('is_live'):
                raise errors.IsLive()

            if info.get('filesize', 0) > MAX_FILESIZE:
                raise errors.OversizeFile()

            ydl.download([url])
            return outtmpl, info

    try:
        return await asyncio.wait_for(asyncio.to_thread(inner), timeout=60)
    except Exception as e:
        raise e


async def send_audio(message: Message, audio_path: str, info: dict) -> None:
    """
    Sends the downloaded audio file to the user.
    """
    title = info.get("title", "Unknown")
    
    thumbnails = info.get("thumbnails", [])
    for t in thumbnails[::-1]:
        try:
            resolution = t.get("resolution")
            height = resolution.split("x")[0]
            height = int(height)

            if height < 320:
                thumbnail = t.get("url")
                break
        except: continue
    else:
        thumbnail = None

    duration = info.get("duration")
    try:
        duration = int(duration) if duration is not None else None
    except (ValueError, TypeError):
        duration = None

    me = await message.bot.get_me()
    await message.answer_audio(
        audio=FSInputFile(audio_path, filename=title),
        duration=duration,
        thumbnail=URLInputFile(thumbnail) if thumbnail else None,
        caption=f"@{me.username}",
    )

