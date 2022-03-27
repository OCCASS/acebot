from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    language = State()
    introduction = State()
    select_games = State()
    age = State()
    who_search = State()
    gender = State()
    looking_for = State()
    country = State()
    region = State()
    city = State()
    name = State()
    about_yourself = State()
    hobby = State()
    photo = State()
    is_correct = State()
    profile = State()
