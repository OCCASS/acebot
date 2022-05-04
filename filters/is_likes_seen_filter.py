from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import BoundFilter

from service.database.api import DatabaseApi

db = DatabaseApi()


class IsLikesSeen(BoundFilter):
    key = "is_likes_seen"

    def __init__(self, is_likes_seen):
        self.is_likes_seen = is_likes_seen

    async def check(self, message: types.Message):
        user = await db.get_user_by_telegram_id(message.from_user.id)
        state = Dispatcher.get_current().current_state(user=message.from_user.id)
        state_data = await state.get_data()
        profile_type = state_data.get('profile_type')
        if profile_type and user:
            profile = await db.get_user_profile(user.telegram_id, profile_type)
            unseen_likes_count = await db.get_unseen_likes_count(profile.id)
            return unseen_likes_count == 0

        return True
