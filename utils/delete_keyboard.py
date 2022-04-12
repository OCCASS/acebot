from aiogram import types


async def delete_keyboard(message: types.Message):
    await message.edit_reply_markup(None)
