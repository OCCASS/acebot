from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from service.database.api import DatabaseApi

db = DatabaseApi()


class BannedUsersMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        from_user_id = message.from_user.id
        if await db.is_user_banned(from_user_id):
            ban_end_datetime = await db.get_user_ban_end_datetime(from_user_id)
            ban_end_datetime_text = 'forever'
            if ban_end_datetime:
                ban_end_datetime_text = 'to ' + str(ban_end_datetime.date())

            await message.answer(f'You are banned {ban_end_datetime_text}', reply_markup=types.ReplyKeyboardRemove())
            raise CancelHandler()
