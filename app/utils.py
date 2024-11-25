from pony.orm import db_session

from .database.models import User

from datetime import datetime
import os


def cleanup_file(file_path: str) -> None:
    """
    Deletes the file from the filesystem.
    """
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")



def spam_checker(user_id: int) -> int:
    with db_session:
        user = User.get(id=user_id)
        now = datetime.now()
        if user.last_request_at:
            dif = now - user.last_request_at
            seconds = int(dif.total_seconds())
            if seconds < 10:
                return 10 - seconds
        user.last_request_at = now
        return 0