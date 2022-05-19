from typing import List

from keyboards.inline.keyboard import get_complain_keyboard, ban_duration_callback
from loader import _
from service.database.models import Profile
from service.get_profile_data import get_profile_data
from service.search import search_profile
from .send import *


async def show_profile_for_accept(profile_data: dict):
    keyboard = await confirm_form.get_keyboard()
    await _show_profile(profile_data, keyboard=keyboard)


async def show_user_profile(*, profile_id: int = None, profile_data: dict = None):
    if profile_id is None and profile_data is None:
        raise TypeError('show_user_profile() require one of two arguments, but no one given')
    elif profile_data and profile_id:
        raise TypeError('show_user_profile() require only one argument, but two was given')

    if profile_id:
        profile = await db.get_profile_by_id(int(profile_id))
        profile_data = await get_profile_data(profile)

    state = dp.current_state()
    await state.update_data(profile_type=profile_data.get('profile_type'))

    keyboard = await profile_form.get_keyboard(row_width=3)
    await _show_profile(profile_data, keyboard)
    await send_profile_options_message()

    state = dp.current_state()
    await state.set_state(States.profile)


async def show_candidate_profile(profile: Profile):
    profile_data = await get_profile_data(profile)
    keyboard = await profile_viewing_form.get_keyboard(row_width=2)
    await _show_profile(profile_data, keyboard=keyboard)


async def pre_show_profile(profile: Profile):
    profile_data = await get_profile_data(profile)
    state = dp.current_state()
    await state.update_data(profile_previewing_type=profile_data.get('profile_type'))
    await show_profile_for_accept(profile_data)


async def show_admirer_profile(profile: Profile, to_user_id=None):
    profile_data = await get_profile_data(profile)
    keyboard = await admirer_profile_viewing_form.get_keyboard(row_width=2)
    await _show_profile(profile_data, keyboard=keyboard, to_user_id=to_user_id)


async def show_your_profile_to_admirer_with_reaction(like_author_profile, user_telegram_id):
    await send_message(_('Ваша анкета кому-то понравилась ❤️!'), user_id=user_telegram_id, reply_markup=None)
    await show_admirer_profile(like_author_profile, to_user_id=user_telegram_id)
    await send_message(_('Ваша реакция отправлена'))


async def show_your_profile_to_admirer_with_message(like_author_profile, user_telegram_id, message):
    await send_message(_('Ваша анкета кому-то понравилась ❤️!'), user_id=user_telegram_id, reply_markup=None)
    await show_admirer_profile(like_author_profile, to_user_id=user_telegram_id)
    await send_message(_('Также тебе отправили сообщение: ') + message, user_id=user_telegram_id)
    await send_message(_('Ваше сообщение отправленно'))


async def show_your_profile_to_another_user(your_profile: Profile, to_user_id: int):
    profile_data = await get_profile_data(your_profile)
    keyboard = await get_complain_keyboard(your_profile.id)
    await _show_profile(profile_data, keyboard=keyboard, to_user_id=to_user_id)


async def show_all_profiles(profiles: List[Profile]):
    for profile in profiles:
        profile_name = await who_search_form.get_by_id(profile.type)
        await send_message(_('Анкета <b>№{profile_num} «{profile_name}»</b>:').format(
            profile_num=profile.type,
            profile_name=_(profile_name.text)))
        await pre_show_profile(profile)


async def show_intruder_profile(profile: Profile):
    keyboard = await ban_duration_form.get_inline_keyboard(ban_duration_callback,
                                                           callback_data_args={'profile_id': profile.id})
    profile_data = await get_profile_data(profile)
    await _show_profile(profile_data, keyboard=ReplyKeyboardRemove())
    complains = await db.get_profile_complains(profile.id)
    message_text = 'Вот жалобы на пользователя:\n'
    for complain in complains:
        ban_text = await complain_type_form.get_by_id(complain.complain_type)
        message_text += _(ban_text.text) + '\n'
    await send_message(message_text, reply_markup=keyboard)


async def find_and_show_profile(user_telegram_id: int):
    state = dp.current_state()
    data = await state.get_data()
    profile_type = data.get('profile_type')
    found_profile_or_none = await search_profile(user_telegram_id, profile_type)
    current_profile = await db.get_user_profile(user_telegram_id, profile_type)
    if found_profile_or_none:
        await show_candidate_profile(found_profile_or_none)

        await db.update_last_seen_profile_id(current_profile.id, found_profile_or_none.id)
        await db.add_or_update_seen_profile(current_profile.id, found_profile_or_none.id)

        await state.update_data(current_viewing_profile_id=found_profile_or_none.id)
        await state.set_state(States.profile_viewing)
    else:
        if current_profile.modification_type is None:
            await send_search_modification_message()
            await state.set_state(States.search_modification)
        else:
            await send_all_profiles_ended()
            await send_profiles_is_ended()
            await send_select_profile_message()
            await state.set_state(States.select_profile)


async def _show_profile(data: dict, keyboard=None, to_user_id=None):
    games_name = []
    for game_id in data.get('games'):
        game = await db.get_game_by_id(game_id)
        games_name.append(game.name)

    gender = await gender_form.get_by_id(data.get('gender'))
    gender = gender.text

    city = await db.get_city_by_id(data.get('city'))
    city = city.name

    text = _('<b>Имя</b>: {name}\n'
             '<b>Возраст</b>: {age}\n'
             '<b>Пол</b>: {gender}\n'
             '<b>Игры</b>: {games}\n'
             '<b>Город</b>: {city}\n'
             '{description}'
             ).format(name=data.get('name'), age=data.get('age'), gender=gender,
                      city=city, description=_(data.get('description')), games=', '.join(games_name))

    await send_message(message_text=text, photo=data.get('photo'), reply_markup=keyboard, user_id=to_user_id)
