

class OversizeFile(Exception):
    def __init__(self, message: str = "The file size is larger than expected."):
        super().__init__(message)


class IsPlaylist(Exception):
    def __init__(self, message: str = "Playlists are not allowed."):
        super().__init__(message)