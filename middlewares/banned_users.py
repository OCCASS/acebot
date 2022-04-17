from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import db


class BannedUsersMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        from_user_id = message.from_user.id
        if await db.is_user_banned(from_user_id):
            await message.answer('You are banned', reply_markup=types.ReplyKeyboardRemove())
            raise CancelHandler()
