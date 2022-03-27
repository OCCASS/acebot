from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.inline.laguage import keyboard
from states import States


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    if not await db.is_user_exists(user_telegram_id):
        from_user = message.from_user
        await db.create_user(user_telegram_id, from_user.full_name, from_user.username)

    await message.answer(
        f'First of all I need to know which language do you speak? It’s will affect only on the menu language!'
        'Прежде всего мне нужно знать, на каком языке вы говорите? Это повлияет только на язык меню!',
        reply_markup=keyboard)
    await state.set_state(States.language)
