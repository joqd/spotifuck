from yt_dlp import YoutubeDL
import httpx

from adagio import bot
from adagio import DOWNLOAD_DIR, COOKIE_FILE

from urllib.parse import urlparse
from pathlib import Path
from typing import Union
from uuid import uuid4
import logging
import os

logger = logging.getLogger(__name__)


def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


def edit_or_send(user_id: int, text: str, n_id: int | None) -> int | None:
    """
    try to edit a notification if n_id provided otherwise send new message.
    returns message id or None
    """
    try:
        if n_id:
            try:
                bot.edit_message_text(text=text, chat_id=user_id, message_id=n_id)
                return n_id
            except Exception:
                msg = bot.send_message(chat_id=user_id, text=text)
                return msg.id
        else:
            msg = bot.send_message(chat_id=user_id, text=text)
            return msg.id
    except Exception:
        return None


def download_audio_by_ytdlp(audio_url: str) -> tuple[str, dict]:
    """
    Downloads the audio from the given YouTube URL and returns the file path.
    """
    outtmpl = (DOWNLOAD_DIR / f'{str(uuid4())}').as_posix()
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'max_filesize': 1000 * (1024 * 1024),
        'outtmpl': outtmpl,
        'noplaylist': True,
    }

    if os.path.exists(COOKIE_FILE):
        ydl_opts['cookiefile'] = COOKIE_FILE

    try:
        with YoutubeDL(ydl_opts) as ydl: # type: ignore
            info = ydl.extract_info(audio_url, download=False)
            info = ydl.sanitize_info(info)

            ydl.download([audio_url])
            return (outtmpl, info) # type: ignore
    except Exception as e:
        logger.exception(e)
        raise e

def download_cover(cover_url: str) -> str | None:
    """Download cover image with httpx; return Path or None"""
    if not cover_url:
        return None

    try:
        with httpx.Client(follow_redirects=True, timeout=10) as client:
            resp = client.get(str(cover_url))
            if resp.status_code == 200 and resp.content:
                outtmpl = (DOWNLOAD_DIR / f'{str(uuid4())}').as_posix()
                filename = outtmpl + "_cover.jpg"
                thumb_path = DOWNLOAD_DIR / filename
                thumb_path.write_bytes(resp.content)
                return thumb_path.as_posix()
    except Exception:
        logger.exception("failed to fetch cover image")
    return None


def safe_unlink(path: Union[str, Path, None]) -> None:
    if not path:
        return
    p = Path(path)
    try:
        if p.exists():
            p.unlink()
    except Exception:
        logger.exception("failed to remove file: %s", str(p))


def is_youtube_url(url: str) -> bool:
    try:
        hostname = urlparse(url).hostname or ""
        return any(h in hostname for h in [
            "youtube.com",
            "youtu.be",
            "youtube-nocookie.com"
        ])
    except Exception:
        return False
