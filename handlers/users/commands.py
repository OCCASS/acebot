from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from service.send import send_language_message, \
    send_select_profile_message, send_help_message, send_no_profile_message
from states import States


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    from_user = message.from_user
    user_telegram_id = from_user.id
    if not await db.is_user_exists(user_telegram_id):
        await db.create_user(user_telegram_id, from_user.full_name, from_user.username)

    await send_language_message()
    await state.set_state(States.language)
    await state.reset_data()


@dp.message_handler(commands=['profiles'], state='*')
async def my_profile(message: types.Message, state: FSMContext):
    profiles = await db.get_user_profiles(message.from_user.id)
    if not profiles:
        await send_no_profile_message()
        await state.set_state(States.language)
    else:
        await send_select_profile_message()
        await state.set_state(States.select_profile)


@dp.message_handler(commands=['help'], state='*')
async def help_command(message: types.Message, state: FSMContext):
    await send_help_message()
