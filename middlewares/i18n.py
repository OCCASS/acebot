from typing import Tuple, Any, Optional

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from service.database.api import DatabaseApi

db = DatabaseApi()


async def get_user_locale(user):
    user_ = await db.get_user_by_telegram_id(user)
    return user_.locale if user_ else 'ru'


class LanguageMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str = '', args=None, user_telegram_id=None) -> Optional[str]:
        if user_telegram_id:
            return await get_user_locale(user_telegram_id)
        elif args is not None and len(args) > 0:
            return await get_user_locale(args[0].from_user.locale)
