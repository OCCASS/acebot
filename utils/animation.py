import asyncio

import aiogram.utils.exceptions
from aiogram import types

from loader import bot, _
from .range import async_range
from .send import send_message


async def loading_animation():
    _message = await send_message('Начинаю обрабатывать ваши данные...', reply_markup=types.ReplyKeyboardRemove())
    async for n in async_range(11):
        await asyncio.sleep(0.2)
        chat_id = types.Chat.get_current().id
        try:
            _message = await bot.edit_message_text(text=_('Обработано {percent}%').format(percent=n * 10),
                                                   chat_id=chat_id,
                                                   message_id=_message.message_id,
                                                   reply_markup=types.ReplyKeyboardRemove())
        except aiogram.utils.exceptions.MessageCantBeEdited:
            break
