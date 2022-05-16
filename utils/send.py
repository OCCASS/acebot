import asyncio
from typing import Union

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BotBlocked

from data.config import ADMINS
from keyboards.default.keyboard import *
from keyboards.inline.keyboard import get_select_profile_keyboard, get_confirm_keyboard
from keyboards.inline.laguage import keyboard as language_keyboard
from loader import bot, _, dp
from service.forms import *
from states import States
from utils.photo_link import photo_link
from utils.profile_link import get_link_to_profile


async def get_chat_id() -> int:
    """This function used to get current chat id"""
    return types.Chat.get_current().id


async def send_message(
        message_text: str,
        reply_markup: Union[
            types.ReplyKeyboardMarkup,
            types.InlineKeyboardMarkup,
            types.ReplyKeyboardRemove] = None,
        parse_mode: str = 'HTML',
        user_id: Union[int, None] = None,
        photo: Union[
            str,
            types.InputFile
        ] = None,
        reply_to_message_id: int = None,
        disable_web_page_preview: bool = True) -> Union[types.Message, None]:
    """
    This function used to send message to user, with default keyboard if keyboard not given in arg
    if user is admin method send message using admin keyboard

    :param message_text: message text, required parameter
    :param reply_markup: keyboard sent with message
    :param parse_mode: message parse mode
    :param user_id: to message user id
    :param photo: photo sent with message
    :param reply_to_message_id: reply to message id
    :param disable_web_page_preview: disable web page preview
    :return: sent message
    """

    try:
        if user_id is None:
            user_id = await get_chat_id()

        if photo:
            return await bot.send_photo(user_id, photo=photo, caption=message_text, parse_mode=parse_mode,
                                        reply_markup=reply_markup, reply_to_message_id=reply_to_message_id)

        return await bot.send_message(user_id, message_text, reply_markup=reply_markup, parse_mode=parse_mode,
                                      reply_to_message_id=reply_to_message_id,
                                      disable_web_page_preview=disable_web_page_preview)
    except BotBlocked:
        return


async def send_incorrect_keyboard_option():
    await send_message(_('Не знаю такой вариант, просьба нажать на одну из кнопок клавиатуры!'))


async def send_gender_message():
    keyboard = await gender_form.get_keyboard()
    await send_message(_('😍 Хм... А неплохо звучит! 😊\n'
                         'Укажи свой пол⬇️'), reply_markup=keyboard)


async def send_choose_games_message(chosen_games):
    keyboard = await get_games_keyboard(chosen_games)
    await send_message(_('Выбери игру 🎮\n'
                         'На следующем шаге ты сможешь добавить ещё одну 😎\n'), reply_markup=keyboard)


async def send_choose_other_games_message(chosen_games):
    keyboard = await get_games_keyboard(chosen_games)
    await send_message(
        _('Хорошшш 👍🏻 Фишка в том, если вы играете еще и в другой пабг, то '
          'можно указать это, что бы искать людей из двух игр или просто жмите  «Продолжить» '),
        reply_markup=keyboard)


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


async def send_name_warning_message(name_length: int):
    await send_message(
        _('Имя должно быть не длиннее 30 символов, текущая длина твоего имени {name_length}! '
          'Введи, пожалуйста, его еще раз').format(name_length=name_length))


async def send_bad_words_or_link_in_name_warning():
    await send_message(_('У тебя в имени есть <b>ссылки</b> или <b>нецензурная брань</b>, исправь, '
                         'пожалуйста, свое имя!'))


async def send_about_your_self_warning():
    await send_message(_('У тебя в тексте есть <b>ссылки</b> или <b>нецензурная брань</b>, исправь, '
                         'пожалуйста, свой рассказ!'))


async def send_hobby_warning():
    await send_message(_('У тебя в хобби есть <b>ссылки</b> или <b>нецензурная брань</b>, исправь, пожалуйста!'))


async def send_is_not_a_photo_message():
    await send_message(_('Отправь мне фото!'), reply_markup=ReplyKeyboardRemove())


async def send_age_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Нам важен Твой возраст🧐'), reply_markup=keyboard)


async def send_name_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Я почти угадал! 😋\n'
                         'Как тебя зовут?'), reply_markup=keyboard)


async def send_country_message():
    keyboard = await get_countries_keyboard()
    await send_message(_('Выберите Страну в которой вы хотите найти друзей🌍'), reply_markup=keyboard)


async def send_city_message(country_id):
    keyboard = await get_cities_keyboard(country_id)
    await send_message(_('Осталось совсем немного 🕐\n'
                         'Укажи свой город 🌁'), reply_markup=keyboard)


async def send_who_search_message(age):
    exceptions = [who_search_form.person_in_real_life.id] if age < 12 else []
    keyboard = await who_search_form.get_keyboard(exceptions=exceptions)
    await send_message(
        _('🛑СТОП🛑\n'
          'Это очень важный пункт, ведь в зависимости от того что ты выберешь у тебя будут 2 '
          '(Команда для праков еще не готова) варианта событий\n\n'
          '1. Человек из реальной жизни - поиск человека из с твоего города, который играет в '
          'такие же игры как ты) Идея вдохновлена одним случаем, когда я познакомился с девочкой в Дай Винчике, у '
          'которой было написано ID, мы поиграли в PUBG, а после пошли гулять\n\n'
          '2. Просто Поиграть - поиск тиммейта из любой страны! Если хочется просто найти человека по интересам '
          'из любой страны, то это идеальный вариант!'
          ),
        reply_markup=keyboard)


async def send_who_looking_for_message():
    keyboard = await who_looking_for_form.get_keyboard()
    await send_message(_('Кого ты ищешь?'), reply_markup=keyboard)


async def send_teammate_country_type_message():
    keyboard = await teammate_country_type_form.get_keyboard()
    await send_message(_('Из какой страны вы хотите чтобы были ваши тимейты'), reply_markup=keyboard)


async def send_about_yourself_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(
        _('Расскажите немного о себе (Сделайте это так, как будто вы слушаете, что о '
          'Тебе говорит ваша вторая половинка на стадии конфетно-букетного периода ваших отношений 🥰😅)'),
        reply_markup=keyboard)


async def send_hobby_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Какие у тебя хобби? 🎨'), reply_markup=keyboard)


async def send_cis_countries_disclaimer_message():
    await send_message(_('Дисклеймер'))


async def send_show_in_random_search_message():
    keyboard = await confirm_form.get_keyboard()
    await send_message(_('Показывать ли вас в рандомном поиске?'), reply_markup=keyboard)


async def send_choose_countries_message(chosen_countries: list):
    keyboard = await get_select_countries_keyboard(chosen_countries)
    await send_message(_('Выбери страну (страны), в которые из которых вы хотите чтобы были ваши тимейты'
                         'После нажатия на одну страну, вы сможете добавить еще одну.'), reply_markup=keyboard)


async def send_play_level_message():
    keyboard = await play_level_form.get_keyboard()
    await send_message(_('Как вы оцениваете свой уровень игры?'), reply_markup=keyboard)


async def send_call_down_message(keyboard=None):
    if keyboard is None:
        keyboard = ReplyKeyboardRemove()

    await send_message(_('Ваше К/Д (через точку)'), reply_markup=keyboard)


async def send_gamer_photo_message():
    keyboard = await get_continue_keyboard()
    await send_message(_('Отправь фото по желанию'), reply_markup=keyboard)


async def send_photo_message():
    await send_message(_('Отправь свое фото, чтобы я смог вставить его в анкету 🖼️'),
                       reply_markup=ReplyKeyboardRemove())


async def send_no_profile_message():
    await send_message(_('У тебя нет анкет, давай создадим! Нажми на /start'), reply_markup=ReplyKeyboardRemove())


async def send_profile_options_message():
    await send_message(_('<b>1.</b> Заполнить анкету заново\n'
                         '<b>2.</b> Изменить фото анкеты\n'
                         '<b>3.</b> Создать новую анкету\n'
                         '<b>4.</b> Начать поиск\n'))


async def send_language_message():
    await send_message(_('Привет! Hello! Вітаю! 👋\n'
                         'Для начала мне нужно узнать, на каком языке тебе показать интерфейс 💻. '
                         'На поиск это никак не повлияет! ☺️ '),
                       reply_markup=language_keyboard)


async def send_select_profile_message():
    keyboard = await get_select_profile_keyboard()
    await send_message(_('У тебя есть несколько анкет разных категорий'), reply_markup=ReplyKeyboardRemove())
    await send_message(_('Выбери какую ты хочешь посмотреть'),
                       reply_markup=keyboard)


async def send_select_profile_type_to_create():
    keyboard = await get_select_profile_keyboard()
    await send_message(_('Выбери тип анкеты, который ты хочешь создать или пересоздать'),
                       reply_markup=keyboard)


async def send_who_search_next_message_and_state(who_search_id):
    state = dp.current_state()
    if who_search_id == who_search_form.person_in_real_life.id:
        await send_who_looking_for_message()
        await state.set_state(States.looking_for)
    elif who_search_id == who_search_form.just_play.id:
        await send_teammate_country_type_message()
        await state.set_state(States.teammate_country_type)
    elif who_search_id == who_search_form.team.id:
        pass


async def send_help_message():
    await send_message(_('Вот команды бота:\n'
                         '/start - команда для начала создание анкеты или для перезапуска бота\n'
                         '/change_match - команда для просмотра списка анкет'))


async def send_profile_photo_was_successfully_edited():
    await send_message(_('Ваша фотография успешно изменена'))


async def send_start_message_writing_to_user():
    await send_message(_('Напиши сообщение, которые ты хочешь отправить:'), reply_markup=ReplyKeyboardRemove())


async def send_email_to_another_user(message_text: str, to_user_id: int):
    await send_message(_('Вам пришло сообщение'), user_id=to_user_id, reply_markup=ReplyKeyboardRemove())
    await send_message(message_text, user_id=to_user_id)
    await send_message(_('Ваша сообщение отправлено!'))


async def send_answer_to_message(message_text: str, to_user_id: int):
    await send_message(_('Вам пришел ответ на ваше сообщение: '), user_id=to_user_id)
    await send_message(message_text, user_id=to_user_id)
    await send_message(_('Ваш ответ оправлен'))


async def send_search_modification_message():
    keyboard = await edit_search_modification_form.get_keyboard()
    await send_message(
        _('Мы пока только развиваемся и пока людей с вашего города с этими параметрами нет, '
          'мы можем предложить вам следующие варианты:'),
        reply_markup=keyboard)


async def send_profiles_is_ended():
    await send_message(_('К сожалению профили закончились'), reply_markup=types.ReplyKeyboardRemove())


async def send_you_have_profiles_message():
    keyboard = await get_confirm_keyboard()
    await send_message(_('Ты перезапустил бота'), reply_markup=types.ReplyKeyboardRemove())
    await send_message(_('У тебя уже были созданные анкеты, не желаешь ли ты их восстановить?'), reply_markup=keyboard)


async def send_reestablish_profile_message():
    keyboard = await reestablish_form.get_keyboard(row_width=2)
    await send_message(_('Восстановить ли эту анкету?'), reply_markup=keyboard)


async def send_you_have_profile_message(profile_name):
    await send_message(_('У тебя есть анкета «{profile_name}»:').format(profile_name=profile_name))


async def start_full_profile_creation():
    state = dp.current_state()
    await send_language_message()
    await state.set_state(States.language)
    await state.reset_data()


async def send_choose_profile_reestablish_type():
    choose_to_reestablish_keyboard = await reestablish_many_from.get_keyboard(row_width=3)
    await send_message(_('Выбери сколько нужно восстановить анкет:'), reply_markup=choose_to_reestablish_keyboard)


async def ask_profile_num_to_reestablish():
    await send_message(_('Напиши номер анкеты, которую надо восстановить'), reply_markup=types.ReplyKeyboardRemove())


async def send_incorrect_profile_num():
    await send_message(_('Не правильный номер анкеты, введи еще раз:'), reply_markup=types.ReplyKeyboardRemove())


async def send_you_have_mutual_sympathy_message(user, admirer_telegram_id):
    profile_link = get_link_to_profile(user.telegram_id)
    link = _('<a href="{profile_link}">{name}</a>').format(profile_link=profile_link, name=user.name)
    await send_message(
        _('У тебя есть взаимная симпатия, вот ссылка на аккаунт {link}, а вот его анкета').format(link=link),
        user_id=admirer_telegram_id, reply_markup=ReplyKeyboardRemove())


async def send_message_with_admirer_telegram_link(admirer_user):
    profile_link = get_link_to_profile(admirer_user.telegram_id)
    link = _('<a href="{profile_link}">{admirer_user_name}</a>').format(profile_link=profile_link,
                                                                        admirer_user_name=admirer_user.name)
    await send_message(_('Вот ссылка на профиль, {link}').format(link=link), reply_markup=types.ReplyKeyboardRemove())


async def send_incorrect_age_message():
    await send_message(_('Твой возраст не подходит для пользования ботом!!!'))


async def send_sleep_message():
    await send_message(_('Пока пока! До встреч! Если твоя анкета кому нибудь понравится, я тебе обязательное скажу!'),
                       reply_markup=types.ReplyKeyboardRemove())


async def send_select_complain_type_form():
    keyboard = await complain_type_form.get_inline_keyboard(exceptions=[complain_type_form.cancel.id])
    await send_message(_('Выбери причину жалобы:'), reply_markup=keyboard)


async def send_your_complain_sent():
    await send_message(_('Твоя жалоба принята!'), reply_markup=types.ReplyKeyboardRemove())


async def send_ban_is_canceled_message():
    await send_message(_('Бан отменен'))


async def send_you_have_likes(user_telegram_id):
    keyboard = await admirer_profile_viewing_form.get_keyboard(row_width=2)
    await send_message(_('Ты понравился еще одному человек, чтобы посмотреть ее оцени прошлую анкету'),
                       user_id=user_telegram_id, reply_markup=keyboard)
    await send_message(_('Ваша реакция отправлена'))


async def send_write_message_to_subs():
    await send_message(_('Напиши сообщение подписчикам: '), reply_markup=ReplyKeyboardRemove())


async def send_message_to_all_subs(message: types.Message):
    users = await db.get_all_users()
    message_text = message.text
    try:
        photo = await photo_link(message.photo[-1])
        message_text = message.caption
    except IndexError:
        photo = None

    tasks = []
    for user in users:
        if user.telegram_id not in ADMINS:
            tasks.append(
                asyncio.create_task(
                    send_message(
                        message_text=message_text,
                        user_id=user.telegram_id,
                        photo=photo)
                )
            )

    await asyncio.gather(*tasks)


async def send_message_is_sent():
    await send_message(_('Сообщение отправлено'))


async def send_support_message():
    await send_message(_('<b>Вы и есть - ACE FAMILY!</b>\n\n'
                         'Мы создали площадку, на которой любой адекватный человек может найти себе '
                         'друзей/девушку/парня (актуально только для парней)/ тиммейтов. Сам процесс разработки бота '
                         'занял у нас долгих 9 месяцев и будет постоянно развиваться, мы можем написать бота, '
                         'придумать кучу разных идей, но у нас нету и не будет средств на масштабную пиар компанию.\n\n'
                         '<i>Что мы придумали?</i>\n\n'
                         'Каждый человек, который как-то расскажет про нашего телеграмм бота или поможет '
                         'донатом будет всегда увековечен в нашем боте и будущих проектах! Мы не хотим '
                         'славы или денег, но без людей проект не проживет - все средства с донатов мы будет '
                         'тратить ТОЛЬКО НА БОТА и что бы в него приходило больше людей.\n\n'
                         'Публикуйте видео с #acetinderbot и мы обязательно будем добавлять всех людей сюда ❤️'))


async def send_second_introduction_message():
    keyboard = await ok_form.get_keyboard()
    await send_message(
        _('❌Сразу тебя предупреждаю, что существует несколько несложных правил, которые необходимо соблюдать:\n'
          '• Анкеты с прокачкой, обменом и продажей аккаунтов – скам, который немедленно улетает в бан. '
          '(Ты ведь знаешь, что лучший сервис для прокачки это @boost_ace 😏);\n'
          '• Запрещено просить других пользователей повысить вашу популярность📈 – за это грозит блокировка;\n'
          '• Категорически запрещается любая пропаганда запрещенных веществ и алкоголя. Также запрещены '
          'дискриминация и оскорбления по расовым/национальным/религиозным признакам ⛔⛔⛔.\n\n'
          '‼️Помни, что именно пользователи создают дружную атмосферу, в которой комфортно находится всем! 😌'),
        reply_markup=keyboard)


async def send_first_introduction_message():
    keyboard = await agree_form.get_keyboard()
    await send_message(
        _('Я создан энтузиастами, которые против того, чтобы ты отдавал свои кровные денежки за возможность '
          'лайкнуть кого-то 😉, поэтому стоит выразить благодарность BOOST ACE за инвестицию в мое создание!⚡ '),
        reply_markup=keyboard)


async def send_profile_creation_ended_message():
    await send_message(
        _('Всё! Просто хочу напомнить тебе, что здесь ты можешь найти не только виртуального, но и вполне реального '
          'друга 🥺. Главное, помни, что на том конце может быть не всегда тот, за кого себя выдает. Удачи! 🍀. '
          'Осталось дело за малым, проверь, пожалуйста, свой профиль, здесь все правильно указано?'))
