from aiogram import Dispatcher

from . import (
    ping,
    youtube_url,
    soundcloud_url,
    spotify_url,
)

def setup(dp: Dispatcher) -> None:
    dp.include_routers(
        ping.router,
        youtube_url.router,
        soundcloud_url.router,
        spotify_url.router,
    )