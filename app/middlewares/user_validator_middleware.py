from aiogram import BaseMiddleware
from pony.orm import db_session
from ..database.models import User

from datetime import datetime


class Middleware(BaseMiddleware):
    def __init__(self, is_callback: bool = False) -> None:
        self.is_callback = is_callback

    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        name = event.from_user.first_name

        with db_session:
            user = User.get(id=user_id)
            if not user:
                user = User(id=user_id, name=name, joined_at=datetime.now())
            if user.name != name:
                user.name = name

        return await handler(event, data)