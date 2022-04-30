from aiogram.dispatcher import FSMContext

from data.types import BanDurationTypes
from keyboards.inline.keyboard import *
from keyboards.inline.laguage import callback as language_callback
from loader import _
from utils.delete_keyboard import delete_keyboard
from utils.notify_complain_admins import notify_complain_admins
from utils.send import *
from utils.show_profile import show_user_profile, pre_show_profile, show_all_profiles, show_intruder_profile


@dp.callback_query_handler(language_callback.filter(), state=States.language)
async def process_language_keyboard(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    locale = callback_data.get('locale')
    await db.set_user_locale(query.from_user.id, locale)

    keyboard = await agree_form.get_keyboard()
    await send_message(
        _('Данный бот создан энтузиастами, у нас нету многолетнего опыта в программирование и создание ботов - '
          'мы просто любим игры и хотели бы найти кого-то из наших городов.\n'
          'В боте никогда не придется платить за то, что бы увидеть кто вам поставил лайк и найти взаимную симпатию, '
          'возможно в будущем мы добавим NFT или какой-то аналог ПОПУЛЯРНОСТИ в PUBGM, но мы сами ненавидим '
          'TINDER/BADOO за то что там надо платить за то, что бы увидеть кто вас лайкнул🤨😥. '
          'На данный момент мы хотим выразить благодарность BOOST ACE за инвестицию в нашу идею!'),
        reply_markup=types.ReplyKeyboardRemove())
    await send_message(
        _('Уважаемые пользователи, существуют всего 3 нерушимых правила, которые запрещены в данном боте. '
          'Мы сами делаем комьюнити, оно состоит из нас, потому попросим вас просто не делать этого:'
          '1 Никакого скама.  Все анкеты с продажей, обменом, прокачкой аккаунтов будут блокироваться! '
          'Не ведитесь вы на скамеров, есть огромное количество мест где вы можете купить/продать ваш аккаунт, '
          'а буст лучше брать у @boost_ace\n'
          '2 Не клянчите ПОПУЛЯРНОСТЬ, тут просто к вам обращусь, не делайте этого. Никому не хочется смотреть '
          'профили “Киньте пожалуйста ПП и ваше айди”, есть много других мест, где вы можете это делать.\n'
          'P.S. Уважаемые пацаны, если вы видите на аватарке милую девушку, у которой выключен '
          'микрофон, то не будьте оленями.\n'
          '3 Пропаганда наркотиков/алкоголя/оружия. Оскорбления по расовому/религиозному признаку, национальному.\n\n'

          'Нас 3 АДМИНОВ, все мы в свое время сидели в Леонардо Дай Винчике и видели какой треш там происходит, '
          'мы не допустим такого в нашем боте и будем четко следить что бы не было троллей/скамеров/фейков.\n\n'

          'Мы и есть комьюнити и если каждый будет стараться сделать что-то лучше, то '
          'надеюсь мы все найдем новых друзей/подруг из игр!'), reply_markup=keyboard)
    await state.set_state(States.introduction)


@dp.callback_query_handler(profile_callback.filter(), state=States.select_profile)
async def process_profile_selection_keyboard(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_telegram_id = query.from_user.id
    profile_type = int(callback_data.get('profile_type'))
    user = await db.get_user_by_telegram_id(user_telegram_id)
    if await db.is_profile_created(user, profile_type):
        profile = await db.get_user_profile(user_telegram_id, profile_type)
        await show_user_profile(profile_id=profile.id)
    else:
        await send_who_search_next_message_and_state(profile_type)
        await state.reset_data()
        await state.update_data(profile_type=profile_type)


@dp.callback_query_handler(answer_to_message_callback.filter(), state='*')
async def process_answer_to_message(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await send_message(_('Введите сообщение:'))
    await state.update_data(to_user_message=int(callback_data.get('user_telegram_id')))
    await state.set_state(States.answering_to_message)


@dp.callback_query_handler(confirm_callback.filter(), state=States.view_created_accounts)
async def process_view_created_profiles(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = query.from_user.id
    confirm_see_profiles_to_reestablish = int(callback_data.get('confirm'))
    if confirm_see_profiles_to_reestablish:
        user_profiles = await db.get_all_user_active_profiles(user_id)
        if len(user_profiles) == 1:  # Если у пользователя всего одна анкета, то сразу показать ее
            profile = user_profiles[0]
            profile_type = await who_search_form.get_by_id(profile.type)
            await send_you_have_profile_message(profile_type.text)
            await pre_show_profile(profile)
            await send_reestablish_profile_message()
            await state.set_state(States.reestablish_profile)
        else:
            await show_all_profiles(user_profiles)
            await send_choose_profile_reestablish_type()
            await state.set_state(States.choose_profiles_to_reestablish)
    else:
        await db.delete_all_user_profiles(user_id)
        await start_full_profile_creation()


@dp.callback_query_handler(complain_callback.filter(), state='*')
async def process_warning_to_profile(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    profile_id = callback_data.get('profile_id')
    keyboard = await complain_type_form.get_inline_keyboard()
    await state.update_data(complain_profile_id=profile_id)
    await query.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(complain_type_form.get_callback_data().filter(), state='*')
async def process_complain_type(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    option_id = int(callback_data.get('id'))
    data = await state.get_data()
    complain_profile_id = int(data.get('complain_profile_id'))

    if option_id == complain_type_form.cancel.id:
        keyboard = await get_complain_keyboard(complain_profile_id)
        await query.message.edit_reply_markup(keyboard)
        return

    profile = await db.get_user_profile(query.from_user.id, data.get('profile_type'))
    await db.create_complain(complain_profile_id, profile.id, option_id)
    await notify_complain_admins(complain_profile_id)
    await delete_keyboard(query.message)
    await send_your_complain_sent()
    await send_select_profile_message()
    await state.set_state(States.select_profile)


@dp.callback_query_handler(show_intruder_profile_callback.filter(), state='*')
async def process_intruder_profile_showing(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    intruder_profile_id = int(callback_data.get('profile_id'))
    intruder_profile = await db.get_profile_by_id(intruder_profile_id)
    await show_intruder_profile(intruder_profile)
    await state.set_state(States.intruder_ban_duration)


@dp.callback_query_handler(ban_duration_callback.filter(), state=States.intruder_ban_duration)
async def process_intruder_ban_duration(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ban_type_id = int(callback_data.get('id'))
    to_profile_id = int(callback_data.get('profile_id'))
    ban_type = None
    if ban_type_id == ban_duration_form.one_day.id:
        ban_type = BanDurationTypes.ONE_DAY
    elif ban_type_id == ban_duration_form.one_month.id:
        ban_type = BanDurationTypes.ONE_MONTH
    elif ban_type_id == ban_duration_form.forever.id:
        ban_type = BanDurationTypes.FOREVER
    elif ban_type_id == ban_duration_form.null.id:
        await delete_keyboard(query.message)
        await send_ban_is_canceled_message()
        return

    await db.create_ban(to_user_telegram_id=query.from_user.id, ban_type=ban_type)
    await db.delete_all_profile_complains(to_profile_id)
    await delete_keyboard(query.message)
