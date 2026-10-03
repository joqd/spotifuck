from django.conf import settings
from spotdl import DownloaderOptions, Spotdl

from app.utils import singleton
from spotifuck import COOKIE_FILE, DOWNLOAD_DIR, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


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
            ),
        )
