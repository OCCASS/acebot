from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.keyboard import get_good_keyboard
from keyboards.inline.keyboard import profile_callback, answer_to_message_callback
from keyboards.inline.laguage import callback as language_callback
from loader import dp, db, _
from states import States
from service.send import send_message, send_who_search_next_message_and_set_state
from service.show_profile import show_user_profile
from service.forms import edit_search_modification_form


@dp.callback_query_handler(language_callback.filter(), state=States.language)
async def process_language_keyboard(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    locale = callback_data.get('locale')
    await db.set_user_locale(query.from_user.id, locale)

    keyboard = await get_good_keyboard()
    await send_message(
        _('Данный бот создан энтузиастами, у нас нету многолетнего опыта в программирование и создание ботов - '
          'мы просто любим игры и хотели бы найти кого-то из наших городов. В боте никогда не придется платить, '
          'что бы увидеть кто вам поставил лайк и найти взаимную симпатию, все будет абсолютно бесплатно и '
          'ограничиваться только железом что бы не было спамеров, но за это будем у вас просить поддержать наши '
          '“возможных” будущих спонсоров и возможно будем держаться на донатах! '
          'На данный момент лучшей поддержкой для нас будет заказать буст у @boost_ace'), reply_markup=keyboard)
    await state.set_state(States.introduction)


@dp.callback_query_handler(profile_callback.filter(), state=States.select_profile)
async def process_profile_selection_keyboard(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_telegram_id = query.from_user.id
    profile_type = int(callback_data.get('profile_type'))
    user = await db.get_user_by_telegram_id(user_telegram_id)
    profile_created = await db.is_profile_created(user, profile_type)
    if profile_created:
        profile = await db.get_user_profile(user_telegram_id, profile_type)
        await show_user_profile(profile_id=profile.id)
        await state.set_state(States.profile)
    else:
        await send_who_search_next_message_and_set_state(profile_type)
        await state.reset_data()
        await state.update_data(profile_type=profile_type)


@dp.callback_query_handler(answer_to_message_callback.filter(), state='*')
async def process_answer_to_message(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await send_message(_('Введите сообщение:'))
    await state.update_data(to_user_message=int(callback_data.get('user_telegram_id')))
    await state.set_state(States.answering_to_message)


@dp.callback_query_handler(edit_search_modification_form.get_callback_data().filter(), state=States.search_modification)
async def process_data_modification(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    field_id = int(callback_data.get('id'))
