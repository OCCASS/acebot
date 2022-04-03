from loader import db
from service.database.models import User, Profile


async def get_profile_data(profile: Profile):
    user = await db.get_user_by_id(profile.user_id)
    profile = await profile.as_dict()
    user = await User.as_dict(user.telegram_id)

    if profile and user:
        data = {}
        for key, value in profile.items():
            data[key] = value
        for key, value in user.items():
            data[key] = value

        return data

    return
