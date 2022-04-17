from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from service.database.models import Ban, User


class BannedUsersMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        from_user_id = message.from_user.id
        user = await User.query.where(User.telegram_id == from_user_id).gino.first()

        if user:
            ban = await Ban.query.where(Ban.to_user_id == user.id)
            if ban:
                await message.answer('You are banned', reply_markup=types.ReplyKeyboardRemove())
                raise CancelHandler()
