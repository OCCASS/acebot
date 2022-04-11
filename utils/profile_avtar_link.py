from loader import bot
from .photo_link import photo_link as get_photo_link


async def get_user_profile_photo(user_id):
    photos = await bot.get_user_profile_photos(user_id)
    photo = None
    if photos.total_count > 0:
        photo = photos.photos[0][0]

    return photo


async def get_user_profile_photo_link(user_id):
    photo = await get_user_profile_photo(user_id)
    photo_link = None
    if photo is not None:
        photo_link = await get_photo_link(photo)

    return photo_link
