from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.forms import who_search_form

profile_callback = CallbackData('profile', 'profile_id')


async def get_select_profile_keyboard(profiles):
    keyboard = InlineKeyboardMarkup()

    for profile in profiles:
        callback = profile_callback.new(str(profile.id))
        profile_name = await who_search_form.get_by_id(profile.type)
        profile_name = profile_name.text
        keyboard.add(InlineKeyboardButton(text=profile_name, callback_data=callback))

    return keyboard
