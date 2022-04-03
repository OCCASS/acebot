from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from service.forms import who_search_form

profile_callback = CallbackData('profile', 'profile_type')
answer_to_message_callback = CallbackData('answer_to', 'user_telegram_id')
modify_search_parameters = CallbackData('modify_search_parameters', 'parameter_id')


async def get_select_profile_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for field in who_search_form.fields:
        callback = profile_callback.new(field.id)
        keyboard.add(InlineKeyboardButton(field.text, callback_data=callback))

    return keyboard


async def get_answer_to_email_keyboard():
    keyboard = InlineKeyboardMarkup()
    user_id = types.User().get_current().id
    callback = answer_to_message_callback.new(str(user_id))
    keyboard.add(InlineKeyboardButton('Ответить', callback_data=callback))
    return keyboard
