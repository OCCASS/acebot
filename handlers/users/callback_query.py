from aiogram.dispatcher import FSMContext

from data.types import BanDurationTypes
from keyboards.inline.keyboard import *
from loader import _
from utils.delete_keyboard import delete_keyboard
from utils.notify_complain_admins import notify_complain_admins
from utils.send import *
from utils.show_profile import pre_show_profile, show_all_profiles, show_intruder_profile


@dp.callback_query_handler(answer_to_message_callback.filter(), state='*')
async def process_answer_to_message(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await send_message(_('Введите сообщение:'))
    await state.update_data(to_user_message=int(callback_data.get('user_telegram_id')))
    await state.set_state(States.answering_to_message)


@dp.callback_query_handler(confirm_callback.filter(), state=States.view_created_accounts)
async def process_view_created_profiles(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = query.from_user.id
    confirm_see_profiles_to_reestablish = int(callback_data.get('confirm'))
    if confirm_see_profiles_to_reestablish:
        user_profiles = await db.get_all_user_active_profiles(user_id)
        if len(user_profiles) == 1:  # Если у пользователя всего одна анкета, то сразу показать ее
            profile = user_profiles[0]
            profile_type = await who_search_form.get_by_id(profile.type)
            await send_you_have_profile_message(profile_type.text)
            await pre_show_profile(profile)
            await send_reestablish_profile_message()
            await state.set_state(States.reestablish_profile)
        else:
            await show_all_profiles(user_profiles)
            await send_choose_profile_reestablish_type()
            await state.set_state(States.choose_profiles_to_reestablish)
    else:
        await db.delete_all_user_profiles(user_id)
        await start_full_profile_creation()


@dp.callback_query_handler(complain_callback.filter(), state='*')
async def process_warning_to_profile(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    profile_id = callback_data.get('profile_id')
    keyboard = await complain_type_form.get_inline_keyboard()
    await state.update_data(complain_profile_id=profile_id)
    await query.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(complain_type_form.get_callback_data().filter(), state='*')
async def process_complain_type(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    option_id = int(callback_data.get('id'))
    data = await state.get_data()
    complain_profile_id = int(data.get('complain_profile_id'))

    if option_id == complain_type_form.cancel.id:
        keyboard = await get_complain_keyboard(complain_profile_id)
        await query.message.edit_reply_markup(keyboard)
        return

    profile = await db.get_user_profile(query.from_user.id, data.get('profile_type'))
    await db.create_complain(complain_profile_id, profile.id, option_id)
    await notify_complain_admins(complain_profile_id)
    await delete_keyboard(query.message)
    await send_your_complain_sent()
    await send_select_profile_message()
    await state.set_state(States.select_profile)


@dp.callback_query_handler(show_intruder_profile_callback.filter(), state='*')
async def process_intruder_profile_showing(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    intruder_profile_id = int(callback_data.get('profile_id'))
    intruder_profile = await db.get_profile_by_id(intruder_profile_id)
    await show_intruder_profile(intruder_profile)
    await state.set_state(States.intruder_ban_duration)


@dp.callback_query_handler(ban_duration_callback.filter(), state=States.intruder_ban_duration)
async def process_intruder_ban_duration(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ban_type_id = int(callback_data.get('id'))
    to_profile_id = int(callback_data.get('profile_id'))
    ban_type = None
    if ban_type_id == ban_duration_form.one_day.id:
        ban_type = BanDurationTypes.ONE_DAY
    elif ban_type_id == ban_duration_form.one_month.id:
        ban_type = BanDurationTypes.ONE_MONTH
    elif ban_type_id == ban_duration_form.forever.id:
        ban_type = BanDurationTypes.FOREVER
    elif ban_type_id == ban_duration_form.null.id:
        await delete_keyboard(query.message)
        await send_ban_is_canceled_message()
        return

    await db.create_ban(to_user_telegram_id=query.from_user.id, ban_type=ban_type)
    await db.delete_all_profile_complains(to_profile_id)
    await delete_keyboard(query.message)


@dp.callback_query_handler(language_callback.filter(), state=States.new_country_language)
async def process_new_country_language(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.delete_reply_markup()
    data = await state.get_data()
    entered_languages = {} if data.get('entered_languages') is None else data.get('entered_languages')

    if callback_data.get('lang') == 'none':
        if entered_languages and data.get('country') is None:
            country = await db.create_country(entered_languages)
            await state.update_data(country=country.id)
        elif entered_languages and data.get('country') is not None:
            await db.update_country_names(data.get('country'), entered_languages)

        data.pop('entered_languages', None)
        data.pop('new_country_lang', None)
        await state.update_data(data)
        await send_message('Спасибо за поддержку!')
        await send_city_message()
        await state.set_state(States.city)
        return

    if callback_data.get('lang') not in entered_languages:
        entered_languages[callback_data.get('lang')] = ''

    await send_message(f'Введи название на <b>{callback_data.get("lang").upper()}</b>:')
    await state.update_data(new_country_lang=callback_data.get('lang'), entered_languages=entered_languages)
    await state.set_state(States.new_country_name)


@dp.callback_query_handler(language_callback.filter(), state=States.new_city_language)
async def process_new_country_language(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.delete_reply_markup()
    data = await state.get_data()
    entered_languages = {} if data.get('entered_languages') is None else data.get('entered_languages')

    if callback_data.get('lang') == 'none':
        if entered_languages and data.get('city') is None:
            city = await db.create_city(entered_languages, data.get('country'))
            await state.update_data(city=city.id)
        elif entered_languages and data.get('city') is not None:
            await db.update_city_names(data.get('city'), entered_languages)

        data.pop('entered_languages', None)
        data.pop('new_city_lang', None)
        await state.update_data(data)
        await send_message('Спасибо за поддержку!')
        await send_who_search_message(data.get('age'))
        await state.set_state(States.who_search)
        return

    if callback_data.get('lang') not in entered_languages:
        entered_languages[callback_data.get('lang')] = ''

    await send_message(f'Введи название на <b>{callback_data.get("lang").upper()}</b>:')
    await state.update_data(new_city_lang=callback_data.get('lang'), entered_languages=entered_languages)
    await state.set_state(States.new_city_name)
