from typing import Union

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.keyboard import *
from loader import db, bot, _
from .forms import *


async def get_chat_id() -> int:
    """This function used to get current chat id"""
    return types.Chat.get_current().id


async def send_message(message_text: str,
                       reply_markup: Union[
                           types.ReplyKeyboardMarkup,
                           types.InlineKeyboardMarkup,
                           types.ReplyKeyboardRemove] = None,
                       parse_mode: str = 'HTML',
                       user_id: int = None,
                       photo: Union[
                           str,
                           types.InputFile
                       ] = None,
                       reply_to_message_id: int = None) -> types.Message:
    """
    This function used to send message to user, with default keyboard if keyboard not given in arg
    if user is admin method send message using admin keyboard

    :param message_text: message text, required parameter
    :param reply_markup: keyboard sent with message
    :param parse_mode: message parse mode
    :param user_id: to message user id
    :param photo: photo sent with message
    :param reply_to_message_id: reply to message id
    :return: sent message
    """

    if not user_id:
        user_id = await get_chat_id()

    if photo:
        return await bot.send_photo(user_id, photo=photo, caption=message_text, parse_mode=parse_mode,
                                    reply_markup=reply_markup, reply_to_message_id=reply_to_message_id)

    return await bot.send_message(user_id, message_text, reply_markup=reply_markup, parse_mode=parse_mode,
                                  reply_to_message_id=reply_to_message_id)


async def send_incorrect_keyboard_option():
    await send_message(_('Не знаю такой вариант, просьба нажать на одну из кнопок клавиатуры!'))


async def send_gender_message():
    keyboard = await gender_form.get_as_keyboard()
    await send_message(_('Выбери свой пол:'), reply_markup=keyboard)


async def send_choose_games_message(chosen_games):
    keyboard = await get_games_keyboard(chosen_games)
    await send_message(_('Выбери игру (игры), в которые вы играете. '
                         'После нажатия на одну игру, вы сможете добавить еще одну.'), reply_markup=keyboard)


async def send_age_warning():
    await send_message(_(
        'Привет, я просто хочу сказать тебе, что в этом мире не все так радужно и '
        'беззаботно, полно злых людей, которые выдают себя не за тех, кем являются'
        ' - никому и никогда не скидывай свои фотографии, никогда не соглашайся на'
        ' встречи вечером или не в людных местах, и подозревай всех) Я просто '
        'переживаю о тебе и береги себя!'
    ))


async def send_int_warning():
    await send_message(_('Введи число!'))


async def send_float_warning():
    await send_message(_('Введи дробное число (через точку, например, 2.4)!'))


async def send_photo_warning():
    await send_message(_('Отправь мне фото!'), reply_markup=ReplyKeyboardRemove())


async def send_age_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Сколько тебе лет?'), reply_markup=keyboard)


async def send_name_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Как тебя зовут?'), reply_markup=keyboard)


async def send_country_message():
    keyboard = await get_countries_keyboard()
    await send_message(_('Из какой ты страны?'), reply_markup=keyboard)


async def send_region_message(country_id):
    keyboard = await get_regions_keyboard(country_id)
    await send_message(_('Из какого ты региона?'), reply_markup=keyboard)


async def send_city_message(region_id):
    keyboard = await get_cities_keyboard(region_id)
    await send_message(_('Из какого ты региона?'), reply_markup=keyboard)


async def send_who_search_message(age):
    exceptions = [who_search_form.person_in_real_life.id] if age < 12 else []
    keyboard = await who_search_form.get_as_keyboard(exceptions=exceptions)
    await send_message(_('Выбери кого ты ищешь?'), reply_markup=keyboard)


async def send_who_looking_for_message():
    keyboard = await who_looking_for_form.get_as_keyboard()
    await send_message(_('Кого ты ищешь?'), reply_markup=keyboard)


async def send_teammate_country_type_message():
    keyboard = await teammate_country_type_form.get_as_keyboard()
    await send_message(_('Из какой страны вы хотите чтобы были ваши тимейты'), reply_markup=keyboard)


async def send_about_yourself_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Расскажи немного о себе:'), reply_markup=keyboard)


async def send_hobby_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Напиши свои хобби:'), reply_markup=keyboard)


async def send_cis_countries_disclaimer_message():
    await send_message(_('Дисклеймер'))


async def send_show_in_random_search_message():
    keyboard = await confirm_form.get_as_keyboard()
    await send_message(_('Показывать ли вас в рандомном поиске?'), reply_markup=keyboard)


async def send_choose_countries_message(chosen_countries: list):
    keyboard = await get_select_countries_keyboard(chosen_countries)
    await send_message(_('Выбери страну (страны), в которые из которых вы хотите чтобы были ваши тимейты'
                         'После нажатия на одну страну, вы сможете добавить еще одну.'), reply_markup=keyboard)


async def send_play_level_message():
    keyboard = await play_level_form.get_as_keyboard()
    await send_message(_('Как вы оцениваете свой уровень игры?'), reply_markup=keyboard)


async def send_call_down_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Ваше К/Д (через точку)'), reply_markup=keyboard)


async def send_gamer_photo_message():
    keyboard = await get_continue_keyboard()
    await send_message(_('Отправь фото по желанию'), reply_markup=keyboard)


async def send_photo_message():
    await send_message(_('Отправь мне свое фото (не файл)'), reply_markup=ReplyKeyboardRemove())
