from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from service.database.api import DatabaseApi

db = DatabaseApi()


class UserInfoChangedMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        from_user_id = message.from_user.id
        user = await db.get_user_by_telegram_id(from_user_id)
        if user:
            if user.username != message.from_user.username:
                await db.update_user_username(from_user_id, message.from_user.username)
