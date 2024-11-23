from aiogram.types import Message, FSInputFile, URLInputFile
from aiogram import Router, F
from yt_dlp import YoutubeDL

from ..settings import DOWNLOAD_DIR
from .. import errors

from uuid import uuid4
import subprocess
import asyncio
import json
import os

router = Router()


# Constants
SPOTIFY_URL_REGEX = r"^(https:\/\/open.spotify.com\/track\/)([a-zA-Z0-9]+)(.*)$"
MAX_FILESIZE = 49 * (1024 * 1024)  # 3 MB
AUDIO_FORMAT = 'm4a'


@router.message(F.text.regexp(SPOTIFY_URL_REGEX))
async def spotify_url(message: Message) -> None:
    """
    Handles messages containing YouTube URLs, downloads the audio, and uploads it.
    """
    alert = await message.answer("Downloading (spotify)...")
    audio_path = None

    try:
        # Download the audio file
        audio_path, info = await download_audio_from_spotify(message.text)
        await alert.edit_text("Uploading...")

        # Send the audio file to the user
        await send_audio(message, audio_path, info)
        await alert.delete()
    except asyncio.TimeoutError:
        await alert.edit_text("Timeout error")
    except Exception as e:
        print(f"Unexpected error: {e}")
        await alert.edit_text("An unexpected error occurred.")
    finally:
        if audio_path:
            cleanup_file(audio_path)


async def download_audio_from_spotify(url: str) -> tuple[str, dict]:
    """
    Downloads the audio from the given Spotify URL and returns the file path and metadata.
    """
    info_path = DOWNLOAD_DIR.as_posix() + f"/{str(uuid4())}.spotdl"
    audio_path = DOWNLOAD_DIR.as_posix() + f"/{str(uuid4())}" + ".{output-ext}"
    command = f"spotdl '{url}' --save-file '{info_path}' --output '{audio_path}' --format mp3"

    def inner():
        _ = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        with open(info_path, "r", encoding="utf-8") as file:
            info = json.load(file)

        try:
            os.remove(info_path)
        except:
            pass
        
        return audio_path.replace("{output-ext}", "mp3"), info[0]
    try:
        return await asyncio.wait_for(asyncio.to_thread(inner), timeout=60)
    except Exception as e:
        raise e


async def send_audio(message: Message, audio_path: str, info: dict) -> None:
    """
    Sends the downloaded audio file to the user.
    """
    title = info.get("name", "Unknown")
    thumbnail = info.get("cover_url")

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
