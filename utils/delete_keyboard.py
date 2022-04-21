from aiogram import types
from aiogram.utils.exceptions import MessageCantBeEdited


async def delete_keyboard(message: types.Message):
    try:
        await message.edit_reply_markup(None)
    except MessageCantBeEdited:
        pass
