from spotdl import Spotdl, DownloaderOptions
from django.conf import settings

from adagio import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, COOKIE_FILE, DOWNLOAD_DIR
from app.utils import singleton


@singleton
class SpotDL:
    def __init__(self):
        self.client = Spotdl(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            downloader_settings=DownloaderOptions(
                cookie_file=COOKIE_FILE,
                output=str(DOWNLOAD_DIR),
                proxy=settings.PROXY,
            )
        )

