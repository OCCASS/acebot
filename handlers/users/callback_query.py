from aiogram.dispatcher import FSMContext

from data.types import ModificationTypes
from keyboards.inline.keyboard import profile_callback, answer_to_message_callback, confirm_callback
from keyboards.inline.laguage import callback as language_callback
from loader import _
from service.send import *
from service.show_profile import show_user_profile, find_and_show_another_user_profile, show_profile, \
    show_all_user_profiles
from states import States


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
        await send_who_search_next_message_and_state(profile_type)
        await state.reset_data()
        await state.update_data(profile_type=profile_type)


@dp.callback_query_handler(answer_to_message_callback.filter(), state='*')
async def process_answer_to_message(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await send_message(_('Введите сообщение:'))
    await state.update_data(to_user_message=int(callback_data.get('user_telegram_id')))
    await state.set_state(States.answering_to_message)


@dp.callback_query_handler(modify_search_parameters.filter(), state=States.search_modification)
async def process_data_modification(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    field_id = int(callback_data.get('id'))
    user_id = query.from_user.id
    data = await state.get_data()
    profile_type = data.get('profile_type')
    modifications = None
    if field_id == edit_search_modification_form.set_target_gender.id:
        modifications = ModificationTypes.GENDER
    elif field_id == edit_search_modification_form.set_target_games.id:
        modifications = ModificationTypes.GAMES
    await db.update_profile_modifications(user_id, profile_type, modifications)
    await find_and_show_another_user_profile(user_id)


@dp.callback_query_handler(confirm_callback.filter(), state=States.view_created_accounts)
async def process_view_created_profiles(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = query.from_user.id
    confirm = int(callback_data.get('confirm'))
    if confirm:
        user_profiles = await db.get_user_profiles(user_id)
        if len(user_profiles) == 1:
            profile = user_profiles[0]
            profile_type = await who_search_form.get_by_id(profile.type)
            await send_you_have_profile_message(profile_type.text)
            await show_profile(profile)
            await send_reestablish_profile_message()
            await state.set_state(States.reestablish_profile)
            return
        else:
            await show_all_user_profiles(user_profiles)
            await send_choose_profile_to_reestablish()
            await state.set_state(States.choose_profiles_to_reestablish)
    else:
        await db.delete_all_user_profiles(user_id)
        await start_full_profile_creation()
