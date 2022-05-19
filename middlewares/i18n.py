from typing import Tuple, Any, Optional

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from service.database.api import DatabaseApi

db = DatabaseApi()


async def get_user_locale(user):
    user_ = await db.get_user_by_telegram_id(user.id)
    return user_.locale if user_ else 'ru'


class LanguageMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        return await get_user_locale(user)
