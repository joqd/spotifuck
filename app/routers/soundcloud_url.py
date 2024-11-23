from aiogram.types import Message, FSInputFile, URLInputFile
from aiogram import Router, F
from yt_dlp import YoutubeDL

from ..settings import DOWNLOAD_DIR
from .. import errors

from uuid import uuid4
import asyncio
import os

router = Router()


# Constants
SOUNDCLOUD_URL_REGEX = r"^(https?:\/\/)?(www\.)?(soundcloud\.com\/[\w\-]+\/[\w\-]+|on\.soundcloud\.com\/[\w]+)(\/?)$"
MAX_FILESIZE = 3 * (1024 * 1024)  # 3 MB
AUDIO_FORMAT = 'm4a'


@router.message(F.text.regexp(SOUNDCLOUD_URL_REGEX))
async def soundcloud_url(message: Message) -> None:
    """
    Handles messages containing SoundCloud URLs, downloads the audio, and uploads it.
    """
    alert = await message.answer("Downloading (soundcloud)...")
    audio_path = None

    try:
        # Download the audio file
        audio_path, info = await download_audio(message.text)
        audio_path += ".m4a"
        await alert.edit_text("Uploading...")
        print(audio_path)

        # Send the audio file to the user
        await send_audio(message, audio_path, info)
        await alert.delete()

    except errors.OversizeFile:
        await alert.edit_text(f"filesize more than {MAX_FILESIZE // (1024 * 1024)}MB")
    except asyncio.TimeoutError:
        await alert.edit_text("Timeout error")
    except Exception as e:
        print(f"Unexpected error: {e}")
        await alert.edit_text("An unexpected error occurred.")
    finally:
        if audio_path:
            cleanup_file(audio_path)


async def download_audio(url: str) -> tuple[str, dict]:
    """
    Downloads the audio from the given SoundCloud URL and returns the file path and metadata.

    :param url: SoundCloud URL to download.
    :return: Tuple containing the file path and metadata.
    :raises ValueError: If file exceeds maximum allowed size or download fails.
    """
    outtmpl = (DOWNLOAD_DIR / f'{str(uuid4())}').as_posix()
    ydl_opts = {
        'format': f'{AUDIO_FORMAT}/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': AUDIO_FORMAT,
        }],
        'max_filesize': MAX_FILESIZE,
        'outtmpl': outtmpl,
        'playlist_items': "1",
    }

    def inner():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info = ydl.sanitize_info(info)

            if info.get('entries'):
                info = info.get('entries')[0]

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

    :param message: Incoming message object.
    :param audio_path: Path to the downloaded audio file.
    :param info: Metadata of the downloaded file.
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

    await message.answer_audio(
        audio=FSInputFile(audio_path, filename=title),
        duration=duration,
        thumbnail=URLInputFile(thumbnail) if thumbnail else None,
    )


def cleanup_file(file_path: str) -> None:
    """
    Deletes the file from the filesystem.
    """
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")
