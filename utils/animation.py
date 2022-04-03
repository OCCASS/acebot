import asyncio

import aiogram.utils.exceptions
from aiogram import types

from loader import bot, _
from utils.range import async_range
from service.send import send_message


async def loading_animation():
    _message = await send_message('Начинаю обрабатывать ваши данные...')
    async for n in async_range(11):
        await asyncio.sleep(0.2)
        chat_id = types.Chat.get_current().id
        try:
            percent = n * 10
            percent_text = f'{percent}%'
            title = _('Обработано')

            if percent >= 70:
                title = _('Подготавливаем картофельные сервера')

            _message = await bot.edit_message_text(
                text='{title} {percent_text}'.format(percent_text=percent_text, title=title),
                chat_id=chat_id,
                message_id=_message.message_id)
        except aiogram.utils.exceptions.MessageCantBeEdited:
            break
