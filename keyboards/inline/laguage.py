from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

callback = CallbackData('language', 'locale')
keyboard = InlineKeyboardMarkup(row_width=3)
keyboard.add(
    InlineKeyboardButton('🇷🇺 Русский', callback_data=callback.new('ru')),
    InlineKeyboardButton('🇬🇧 English', callback_data=callback.new('en'))
)
