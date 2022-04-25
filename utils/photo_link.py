from io import BytesIO
from urllib.parse import urljoin

from aiogram import types

from loader import bot


async def photo_link(photo: types.photo_size.PhotoSize) -> str:
    file = await photo.download(destination_file=BytesIO())
    session = await bot.get_session()
    async with session.post('https://telegra.ph/upload', data={'file': file}) as response:
        img_src = await response.json()
        response.close()

    link = urljoin('https://telegra.ph/', img_src[0]["src"])
    return link
