from loader import _
from .data_unifier import unify_data
from .database.models import Profile
from .get_profile_data import get_profile_data
from .search import search_profile
from .send import *


async def show_profile_for_accept(profile_data: dict):
    await _show_profile(profile_data)


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


async def show_another_user_profile(profile: Profile):
    profile_data = await get_profile_data(profile)
    keyboard = await profile_viewing_form.get_keyboard(2)
    await _show_profile(profile_data, keyboard=keyboard)


async def show_profile(profile: Profile):
    profile_data = await get_profile_data(profile)
    state = dp.current_state()
    await state.update_data(profile_previewing_type=profile_data.get('profile_type'))
    await _show_profile(profile_data, keyboard=None)


async def show_admirer_profile(profile: Profile):
    profile_data = await get_profile_data(profile)
    keyboard = await admirer_profile_viewing.get_keyboard(row_width=2)
    await _show_profile(profile_data, keyboard=keyboard)


async def show_all_user_profiles(profiles):
    for profile_index, profile in enumerate(profiles):
        profile_name = await who_search_form.get_by_id(profile.type)
        await send_message(_(f'Анкета <b>№{profile_index + 1} «{profile_name.text}»</b>:'))
        await show_profile(profile)


async def find_and_show_another_user_profile(user_telegram_id: int):
    state = dp.current_state()
    data = await state.get_data()
    profile_type = data.get('profile_type')
    profile = await search_profile(user_telegram_id, profile_type)
    curren_profile = await db.get_user_profile(user_telegram_id, profile_type)
    if profile:
        await show_another_user_profile(profile)
        await db.update_last_seen_profile_id(user_telegram_id, profile.id)
        await state.update_data(current_viewing_profile_id=profile.id)
        await state.set_state(States.profile_viewing)
    else:
        if curren_profile.modification_type is None:
            await send_search_modification_message()
            await state.set_state(States.search_modification)
        else:
            await send_profiles_is_ended()
            await send_select_profile_message()
            await state.set_state(States.select_profile)


async def _show_profile(data: dict, keyboard=None):
    games = []
    for game_id in data.get('games'):
        game = await db.get_game_by_id(game_id)
        games.append(game.name)

    games = list(map(lambda i: f'<b>{i}</b>', games))
    games_text = ', '.join(games)

    gender = await gender_form.get_by_id(data.get('gender'))
    gender = gender.text

    city = await db.get_city_by_id(data.get('city'))
    city = city.name

    text = _('Имя: <b>{name}</b>\n'
             'Возраст: <b>{age}</b>\n'
             'Пол: <b>{gender}</b>\n'
             'Игры: {games}\n'
             'Город: <b>{city}</b>\n'
             '{description}'
             ).format(name=data.get('name'), age=data.get('age'), gender=gender,
                      city=city, description=data.get('description'), games=games_text)

    if keyboard is None:
        keyboard = await confirm_form.get_keyboard()

    await send_message(message_text=text, photo=data.get('photo'), reply_markup=keyboard)
