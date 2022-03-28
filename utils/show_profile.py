from .profile import get_profile_data
from .send import send_message, send_profile_options_message
from loader import db, _
from .forms import *


async def show_profile(data: dict, keyboard=None):
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
        keyboard = await confirm_form.get_as_keyboard()

    await send_message(message_text=text, photo=data.get('photo'), reply_markup=keyboard)


async def show_profile_for_accept(profile_data: dict):
    await show_profile(profile_data)


async def show_user_profile(*, profile_id: int = None, profile_data: dict = None):
    if profile_id is None and profile_data is None:
        raise TypeError('show_user_profile() require one of two arguments, but no one given')
    elif profile_data and profile_id:
        raise TypeError('show_user_profile() require only one argument, but two was given')

    if profile_id:
        profile = await db.get_profile_by_id(int(profile_id))
        profile_data = await get_profile_data(profile)

    keyboard = await profile_form.get_as_keyboard(row_width=3)
    await show_profile(profile_data, keyboard)
    await send_profile_options_message()
