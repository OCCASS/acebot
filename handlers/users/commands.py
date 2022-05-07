from aiogram.dispatcher import FSMContext

from utils.send import *
from states import States


@dp.message_handler(commands=['start'], is_likes_seen=True, state='*')
async def start(message: types.Message, state: FSMContext):
    from_user = message.from_user
    user_telegram_id = from_user.id

    if not await db.is_user_exists(user_telegram_id):
        await db.create_user(user_telegram_id, from_user.full_name, from_user.username)

    user_profiles = await db.get_all_user_active_profiles(user_telegram_id)
    if len(user_profiles) > 0:
        await send_you_have_profiles_message()
        await state.set_state(States.view_created_accounts)
        return

    await start_full_profile_creation()


@dp.message_handler(ommands=['change_match'], is_likes_seen=True, cstate='*')
async def my_profile(message: types.Message, state: FSMContext):
    profiles = await db.get_all_user_active_profiles(message.from_user.id)
    if not profiles:
        await send_no_profile_message()
        await state.set_state(States.language)
    else:
        await send_select_profile_message()
        await state.set_state(States.select_profile)


@dp.message_handler(commands=['help'], is_likes_seen=True, state='*')
async def help_command(message: types.Message, state: FSMContext):
    await send_help_message()
