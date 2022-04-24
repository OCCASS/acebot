from aiogram.dispatcher.filters import Filter
from aiogram import types
from data.config import ADMINS


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: types.Message):
        return message.from_user.id in ADMINS
