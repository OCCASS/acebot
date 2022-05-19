from loader import bot


async def get_user_profile_photo(user_id):
    photos = await bot.get_user_profile_photos(user_id)
    photo = None
    if photos.total_count > 0:
        photo = photos.photos[0][0].file_id

    return photo
