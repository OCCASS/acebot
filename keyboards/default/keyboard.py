from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db, _


async def get_continue_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(KeyboardButton(_('Продолжить')))
    return keyboard


async def get_games_keyboard(selected_games):
    games_list = await db.get_all_games()

    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for game in games_list:
        if game.id not in selected_games:
            keyboard.add(KeyboardButton(text=game.name))

    if len(selected_games) > 0:
        keyboard.add(KeyboardButton(_('Продолжить')))

    return keyboard


async def get_select_countries_keyboard(selected_countries):
    all_countries = await db.get_all_countries()

    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for country in all_countries:
        if country.id not in selected_countries:
            keyboard.add(KeyboardButton(text=country.name))

    if len(selected_countries) > 0:
        keyboard.add(KeyboardButton(_('Продолжить')))

    return keyboard


async def get_countries_keyboard():
    all_countries = await db.get_all_countries()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for country in all_countries:
        keyboard.add(KeyboardButton(text=_(country.name)))

    return keyboard


async def get_cities_keyboard(region_id: int):
    all_cities = await db.get_cities_by_region(region_id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for city in all_cities:
        keyboard.add(KeyboardButton(text=_(city.name)))

    return keyboard
