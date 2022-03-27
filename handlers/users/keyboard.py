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
from utils.validate import is_int, is_float
from utils.send import send_incorrect_keyboard_option, send_message, send_gender_message
from utils.forms import *
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
    await send_message(_('Как тебя зовут?'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.name)


@dp.message_handler(state=States.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await send_gender_message()
    await state.set_state(States.gender)


@dp.message_handler(state=States.gender)
async def process_gender(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await gender_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    gender_id = await gender_form.get_id_by_text(user_answer)
    await state.update_data(gender=gender_id)

    keyboard = await who_search_form.get_as_keyboard()
    await send_message(_('Выбери кого ты ищешь?'), reply_markup=keyboard)
    await state.set_state(States.who_search)


@dp.message_handler(state=States.who_search)
async def process_who_search(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await who_search_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    who_search_id = await who_search_form.get_id_by_text(user_answer)
    await state.update_data(profile_type=who_search_id)

    if who_search_id == who_search_form.person_in_real_life.id:
        keyboard = await who_looking_for_form.get_as_keyboard()
        await send_message(_('Кого ты ищешь?'), reply_markup=keyboard)
        await state.set_state(States.looking_for)
        return
    elif who_search_id == who_search_form.just_play.id:
        keyboard = await teammate_country_type_form.get_as_keyboard()
        await send_message(_('Из какой страны вы хотите чтобы были ваши тимейты'), reply_markup=keyboard)
        await state.set_state(States.teammate_country_type)
        return
    elif who_search_id == who_search_form.team.id:
        pass


@dp.message_handler(state=States.looking_for)
async def process_looking_for(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await who_looking_for_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    who_looking_for_id = await who_looking_for_form.get_id_by_text(user_answer)
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

    if not await confirm_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    is_correct = await confirm_form.get_id_by_text(user_answer)
    if is_correct == confirm_form.yes.id:
        await db.update_user(from_user_id,
                             data.get('name'),
                             data.get('gender'),
                             data.get('city'),
                             data.get('age'),
                             data.get('games'))
        await send_message('Заглушка для поиска...')
        await state.reset_data()
    else:
        keyboard = await profile_form.get_as_keyboard(row_width=3)
        await show_profile(data, keyboard=keyboard)
        await state.set_state(States.profile)
        await state.reset_data()


@dp.message_handler(state=States.teammate_country_type)
async def process_teammate_country_type(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await teammate_country_type_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    teammate_country_type_id = await teammate_country_type_form.get_id_by_text(user_answer)
    await state.update_data(teammate_country_type=teammate_country_type_id)

    # Если пользователь выбрал "Страны СНГ"
    if teammate_country_type_id == teammate_country_type_form.cis_countries.id:
        cis_countries = await db.get_cis_countries()
        cis_countries_ids = [country.id for country in cis_countries]
        await state.update_data(search_countries=cis_countries_ids)
        await send_message(_('Дисклеймер'))
        keyboard = await confirm_form.get_as_keyboard()
        await send_message(_('Показывать ли вас в рандомном поиске?'), reply_markup=keyboard)
        await state.set_state(States.show_in_random_search)
        return
    # Если пользователь выбрал "Выбрать страну"
    elif teammate_country_type_id == teammate_country_type_form.select_country.id:
        search_countries = []
        await state.update_data(search_countries=search_countries)
        keyboard = await get_select_countries_keyboard(search_countries)
        await send_message('Выбери страны', reply_markup=keyboard)
        await state.set_state(States.select_countries)
    # Если пользователь выбрал "Любая страна"
    elif teammate_country_type_id == teammate_country_type_form.random_country.id:
        all_countries = await db.get_all_countries()
        all_countries_ids = [country.id for country in all_countries]
        await state.update_data(search_countries=all_countries_ids)
        keyboard = await play_level_form.get_as_keyboard()
        await send_message(_('Как вы оцениваете свой уровень игры?'), reply_markup=keyboard)
        await state.set_state(States.play_level)


@dp.message_handler(state=States.select_countries)
async def process_country_selection(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await validate_select_countries_keyboard(user_answer):
        await send_incorrect_keyboard_option()
        return

    if await validate_continue_keyboard(user_answer):
        keyboard = await confirm_form.get_as_keyboard()
        await send_message(_('Показывать ли вас в рандомном поиске?'), reply_markup=keyboard)
        await state.set_state(States.show_in_random_search)
        return

    country_id = await db.get_country_id_by_name(user_answer)
    data = await state.get_data()
    data['search_countries'].append(country_id)
    await state.update_data(data)

    keyboard = await get_select_countries_keyboard(data.get('search_countries'))
    await send_message('Выбери еще страны или нажми продолжить', reply_markup=keyboard)


@dp.message_handler(state=States.show_in_random_search)
async def process_show_in_random_search(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await confirm_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    show_in_random_search = await confirm_form.get_id_by_text(user_answer)

    if show_in_random_search == confirm_form.yes.id:
        await state.update_data(show_in_random_search=True)
    else:
        await state.update_data(show_in_random_search=False)

    keyboard = await play_level_form.get_as_keyboard()
    await send_message(_('Как вы оцениваете свой уровень игры?'), reply_markup=keyboard)
    await state.set_state(States.play_level)


@dp.message_handler(state=States.play_level)
async def process_play_level(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await play_level_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    play_level_id = await play_level_form.get_id_by_text(user_answer)
    await state.update_data(play_level=play_level_id)

    await send_message(_('Ваше К/Д (через точку)'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.call_down)


@dp.message_handler(state=States.call_down)
async def process_user_call_down(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await is_float(user_answer):
        await send_message(_('Введи число, если дробное, то через точку'))
        return

    await state.update_data(call_down=float(user_answer))
    await send_message(_('Что-то от себя:'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.something_about_yourself)


@dp.message_handler(state=States.something_about_yourself)
async def process_something_about_yourself(message: types.Message, state: FSMContext):
    await state.update_data(about_yourself=message.text)
    keyboard = await get_continue_keyboard()
    await send_message(_('Отправь фото по желанию'), reply_markup=keyboard)
    await state.set_state(States.gamer_photo)


@dp.message_handler(state=States.gamer_photo, content_types=types.ContentTypes.ANY)
async def process_gamer_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        photo = None
    else:
        photo = photo_link(message.photo[-1])

    await state.update_data(photo=photo)
    await loading_animation()

    data = await state.get_data()
    data['country'] = None
    data['region'] = None
    data['city'] = 1
    data = await process_data(data)
    await show_profile(data)
    await state.set_state(States.is_correct)
