from .send import send_message
from loader import db, _
from .menus import *


async def show_profile(data: dict, keyboard=None):
    games = []
    for game_id in data.get('games'):
        game = await db.get_game_by_id(game_id)
        games.append(game.name)

    games_text = '<b>' + '</b>, <b>'.join(games) + '</b>'

    gender = await gender_menu.get_by_id(data.get('gender'))
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

    keyboard = await is_correct_menu.get_as_keyboard() if keyboard is None else keyboard
    await send_message(
        message_text=text,
        photo=data.get('photo'),
        reply_markup=keyboard
    )
