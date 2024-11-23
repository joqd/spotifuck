

class OversizeFile(Exception):
    def __init__(self, message: str = "The file size is larger than expected."):
        super().__init__(message)


class IsLive(Exception):
    def __init__(self, message: str = "Live stream are not allowed."):
        super().__init__(message)