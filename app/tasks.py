from celery import shared_task

from adagio import bot
from adagio import HISTORY_CHANNEL
from app.spotdl_client import SpotDL
from app.models import User, Download
from app.utils import safe_unlink
from app.utils import edit_or_send
from app.utils import is_youtube_url
from app.utils import download_cover
from app.utils import download_audio_by_ytdlp

import os
import time


@shared_task
def downloader(query: str, user_id: int, n_id: int | None = None):
    n_id = edit_or_send(user_id=user_id, text='- Searching...', n_id=n_id,)

    spotdl = SpotDL().client

    songs = spotdl.search([query])
    if not songs:
        n_id = edit_or_send(user_id=user_id, text='Not found.', n_id=n_id)
        return {'ok': False, 'error': 'not found'}
    song = songs[0]

    n_id = edit_or_send(user_id=user_id, text=f'- Extract download link...', n_id=n_id)
    
    if not is_youtube_url(query):
        urls = spotdl.get_download_urls([song])

        if not urls or type(urls[0]) != str:
            n_id = edit_or_send(user_id=user_id, text='Failed to extract download link.', n_id=n_id)
            return {'ok': False, 'error': 'failed to extract download urls'}
        url = urls[0]
    else:
        url = query

    n_id = edit_or_send(user_id=user_id, text='- Downloading...', n_id=n_id)

    try:
        path, info = download_audio_by_ytdlp(url)
        path += '.mp3'

        title = info.get("title", "Unknown")

        duration = info.get("duration")
        try:
            duration = int(duration) if duration is not None else None
        except (ValueError, TypeError):
            duration = None

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
    except:
        n_id = edit_or_send(user_id=user_id, text='Failed to download.', n_id=n_id)
        return {'ok': False, 'error': 'failed to download'}

    cover_url = thumbnail
    if cover_url:
        cover_path = download_cover(cover_url)

    n_id = edit_or_send(user_id=user_id, text='- Uploading...', n_id=n_id)

    try:
        with open(path, "rb") as audio:
            if cover_path and os.path.exists(cover_path):
                with open(cover_path, "rb") as thumb:
                    message = bot.send_audio(
                        chat_id=user_id, 
                        audio=audio, 
                        thumb=thumb,
                        title=title,
                        duration=duration,
                    )
            else:
                message = bot.send_audio(
                    chat_id=user_id, 
                    audio=audio,
                    title=title,
                    duration=duration,
                )

        try:
            download_message_id = bot.copy_message(chat_id=HISTORY_CHANNEL, from_chat_id=user_id, message_id=message.id)
            download_message_id = download_message_id.message_id
        except:
            download_message_id = None

        try:
            user = User.objects.get(id=user_id)
            Download.objects.create(
                user=user,
                query=query,
                message_id=download_message_id,
            )
        except User.DoesNotExist:
            pass

    except Exception as e:
        n_id = edit_or_send(
            user_id=user_id,
            text='Failed to upload.',
            n_id=n_id,
        )
        return {"ok": False, "error": str(e)}
    finally:
        try:
            if path and os.path.exists(path):
                safe_unlink(path)
            
            if cover_path and os.path.exists(cover_path):
                safe_unlink(cover_path)
        except Exception:
            pass

    if n_id:
        bot.delete_message(chat_id=user_id, message_id=n_id)

    return {'ok': True}


@shared_task
def send_message_to_all_users(from_chat_id: int, message_id: int):
    n_id = edit_or_send(from_chat_id, 'please wait...', None)

    total = 0
    success = 0

    users = User.objects.all()
    users_counts = users.count() - 1

    for user in users:
        if user.id == from_chat_id:
            continue

        try:
            bot.copy_message(
                chat_id=user.id,
                from_chat_id=from_chat_id,
                message_id=message_id,
            )

            success += 1
        finally:
            total += 1

            if total % 100 == 0:
                time.sleep(1)
                n_id = edit_or_send(from_chat_id, f'sent for {success}/{users_counts}', n_id)
            else:
                time.sleep(0.25)

    n_id = edit_or_send(from_chat_id, f'sent for {success}/{users_counts}', n_id)


@shared_task
def random_nightly_music():
    bot.send_message(chat_id=5479189128, text='fuck you in 22.')