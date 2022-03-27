from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.keyboard import *
from loader import dp, _
from states import States
from utils.animation import loading_animation
from utils.process_data import process_data
from utils.show_profile import show_profile
from utils.validate_keyboard_answer import *
from utils.validate import is_int
from utils.send import send_incorrect_keyboard_option, send_message
from utils.menus import *
from utils.photo_link import photo_link


@dp.message_handler(state=States.introduction)
async def process_introduction(message: types.Message, state: FSMContext):
    if not await validate_good_keyboard(message.text):
        await send_incorrect_keyboard_option()
        return

    games = []
    keyboard = await get_games_keyboard(games)
    await send_message(_('Выбери игры из списка'), reply_markup=keyboard)
    await state.update_data(games=games)
    await state.set_state(States.select_games)


@dp.message_handler(state=States.select_games)
async def process_games(message: types.Message, state: FSMContext):
    user_answer = message.text

    # Если пользователь нажал на кнопку не с клавиатуры
    if not await validate_games_keyboard(user_answer):
        await send_incorrect_keyboard_option()
        return

    # Если пользователь нажал на продолжить
    if await validate_continue_keyboard(user_answer):
        await send_message(_('Сколько тебе лет?'), reply_markup=ReplyKeyboardRemove())
        await state.set_state(States.age)
        return

    # Если пользователь нажал на игру
    game = await db.get_game_by_name(user_answer)
    data = await state.get_data()
    data['games'].append(game.id)
    await state.update_data(data)

    keyboard = await get_games_keyboard(data['games'])
    await send_message(_('Выбери еще игры'), reply_markup=keyboard)


@dp.message_handler(state=States.age)
async def process_age(message: types.Message, state: FSMContext):
    user_answer = message.text
    if not await is_int(user_answer):
        await send_message(_('Введите число!'))
        return

    age = int(user_answer)
    if age < 16:
        await send_message(_(
            'Привет, я просто хочу сказать тебе, что в этом мире не все так радужно и '
            'беззаботно, полно злых людей, которые выдают себя не за тех, кем являются'
            ' - никому и никогда не скидывай свои фотографии, никогда не соглашайся на'
            ' встречи вечером или не в людных местах, и подозревай всех) Я просто '
            'переживаю о тебе и береги себя!'
        ))

    await state.update_data(age=int(user_answer))
    keyboard = await who_search_menu.get_as_keyboard()
    await send_message(_('Выбери кого ты ищешь?'), reply_markup=keyboard)
    await state.set_state(States.who_search)


@dp.message_handler(state=States.who_search)
async def process_who_search(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await who_search_menu.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    who_search_id = await who_search_menu.get_id_by_text(user_answer)
    await state.update_data(profile_type=who_search_id)

    if who_search_id == who_search_menu.person_in_real_life.id:
        keyboard = await gender_menu.get_as_keyboard(row_width=2)
        await send_message(_('Выбери свой пол:'), keyboard)
        await state.set_state(States.gender)
        return
    elif who_search_id == who_search_menu.team.id:
        pass
    elif who_search_id == who_search_menu.just_play.id:
        pass


@dp.message_handler(state=States.gender)
async def process_gender(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await gender_menu.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    gender_id = await gender_menu.get_id_by_text(user_answer)
    await state.update_data(gender=gender_id)

    keyboard = await who_looking_for_menu.get_as_keyboard()
    await send_message(_('Кого ты ищешь?'), reply_markup=keyboard)
    await state.set_state(States.looking_for)


@dp.message_handler(state=States.looking_for)
async def process_looking_for(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await who_looking_for_menu.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    who_looking_for_id = await who_looking_for_menu.get_id_by_text(user_answer)
    await state.update_data(who_looking_for=who_looking_for_id)

    keyboard = await get_countries_keyboard()
    await send_message(_('Из какой ты страны?'), reply_markup=keyboard)
    await state.set_state(States.country)


@dp.message_handler(state=States.country)
async def process_country(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await validate_countries_keyboard(user_answer):
        await send_incorrect_keyboard_option()
        return

    country_id = await db.get_country_id_by_name(user_answer)
    await state.update_data(country=country_id)

    keyboard = await get_regions_keyboard(country_id)
    await send_message(_('Выбери свой регион:'), reply_markup=keyboard)
    await state.set_state(States.region)


@dp.message_handler(state=States.region)
async def process_region(message: types.Message, state: FSMContext):
    user_answer = message.text

    data = await state.get_data()
    if not await validate_regions_keyboard(user_answer, data.get('country')):
        await send_incorrect_keyboard_option()
        return

    region_id = await db.get_region_id_by_name(user_answer)
    await state.update_data(region=region_id)

    keyboard = await get_cities_keyboard(region_id)
    await send_message(_('Из какого ты города?'), reply_markup=keyboard)
    await state.set_state(States.city)


@dp.message_handler(state=States.city)
async def process_city(message: types.Message, state: FSMContext):
    user_answer = message.text

    data = await state.get_data()
    if not await validate_cities_keyboard(user_answer, data.get('region')):
        await send_incorrect_keyboard_option()
        return

    city_id = await db.get_city_id_by_name(user_answer)
    await state.update_data(city=city_id)

    await send_message(_('Как тебя зовут?'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.name)


@dp.message_handler(state=States.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await send_message(_('Расскажи о себе'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.about_yourself)


@dp.message_handler(state=States.about_yourself)
async def process_about_yourself(message: types.Message, state: FSMContext):
    await state.update_data(about_yourself=message.text)

    await send_message(_('Хобби'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.hobby)


@dp.message_handler(state=States.hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    await state.update_data(hobby=message.text)

    await send_message(_('Отправь мне свое фото (не файл)'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.photo)


@dp.message_handler(state=States.photo, content_types=types.ContentTypes.ANY)
async def process_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await send_message('Отправь мне фото!')
        return

    photo_link_ = await photo_link(message.photo[-1])
    await state.update_data(photo=photo_link_)
    await loading_animation()

    data = await state.get_data()
    data = await process_data(data)
    await show_profile(data)
    await state.set_state(States.is_correct)


@dp.message_handler(state=States.is_correct, content_types=types.ContentTypes.ANY)
async def process_is_profile_correct(message: types.Message, state: FSMContext):
    user_answer = message.text
    from_user_id = message.from_user.id
    data = await state.get_data()

    if not await is_correct_menu.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    is_correct = await is_correct_menu.get_id_by_text(user_answer)
    if is_correct == is_correct_menu.yes.id:
        await db.update_user(from_user_id,
                             data.get('name'),
                             data.get('gender'),
                             data.get('city'),
                             data.get('age'),
                             data.get('games'))
        await send_message('Заглушка для поиска...')
        # await db.create_profile_if_not_exists_else_update(
        #     from_user_id, data.get('who_search'), data.get('photo'), data.get('description')
        # )
        await state.reset_data()
    else:
        keyboard = await profile_menu.get_as_keyboard(row_width=3)
        await show_profile(data, keyboard=keyboard)
        await state.set_state(States.profile)
        await state.reset_data()
