from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from service.forms import who_search_form
from loader import _

profile_callback = CallbackData('profile', 'profile_type')
answer_to_message_callback = CallbackData('answer_to', 'user_telegram_id')
confirm_callback = CallbackData('confirm', 'confirm')
complain_callback = CallbackData('warning', 'profile_id')
show_intruder_profile_callback = CallbackData('show_intruder_profile', 'profile_id')
ban_duration_callback = CallbackData('ban_duration', 'id', 'profile_id')


async def get_complain_keyboard(profile_id):
    warning_keyboard = types.InlineKeyboardMarkup()
    warning_keyboard.add(
        InlineKeyboardButton(_('Пожаловаться ⚠️'), callback_data=complain_callback.new(profile_id=profile_id)))
    return warning_keyboard


async def get_select_profile_keyboard(locale=None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for field in who_search_form.fields:
        callback = profile_callback.new(field.id)
        keyboard.add(InlineKeyboardButton(_(field.text, locale=locale), callback_data=callback))

    return keyboard


async def get_answer_to_email_keyboard():
    keyboard = InlineKeyboardMarkup()
    user_id = types.User().get_current().id
    callback = answer_to_message_callback.new(str(user_id))
    keyboard.add(InlineKeyboardButton(_('Ответить'), callback_data=callback))
    return keyboard


async def get_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(InlineKeyboardButton(text=_('Да'), callback_data=confirm_callback.new(1)),
                 InlineKeyboardButton(text=_('Нет'), callback_data=confirm_callback.new(0)))
    return keyboard


async def get_show_intruder_profile_keyboard(intruder_profile_id: int):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(_('Показать профиль нарушителя 👁'),
                                      callback_data=show_intruder_profile_callback.new(intruder_profile_id)))
    return keyboard
