from aiogram.dispatcher import FSMContext

from data.config import WARNING_AGE
from data.types import ModificationTypes
from service.data_unifier import unify_data
from service.validate import is_int, is_float, validate_age
from service.validate_keyboard_answer import *
from utils.animation import loading_animation
from utils.delete_keyboard import delete_keyboard
from utils.photo_link import photo_link as get_photo_link
from utils.send import *
from utils.show_profile import show_profile_for_accept, show_user_profile, find_and_show_profile, \
    show_your_profile_to_another_user, show_your_profile_to_admirer_with_reaction, show_admirer_profile


@dp.message_handler(state=States.introduction)
async def process_introduction(message: types.Message, state: FSMContext):
    if not await agree_form.validate_message(message.text):
        await send_incorrect_keyboard_option()
        return

    games = []
    await send_choose_games_message(games)
    await state.update_data(games=games)
    await state.set_state(States.select_games)


@dp.message_handler(state=States.select_games)
async def process_games_selection(message: types.Message, state: FSMContext):
    user_answer = message.text
    data = await state.get_data()

    # Если пользователь нажал на кнопку не с клавиатуры
    if not await validate_games_keyboard(user_answer):
        await send_incorrect_keyboard_option()
        return

    # Если пользователь нажал на игру
    game = await db.get_game_by_name(user_answer)
    if game:
        data['games'].append(game.id)
        data['games'] = list(set(data['games']))

    all_games = await db.get_all_games()
    is_all_games_selected = len(data.get('games')) == len(all_games)
    is_continue_button_clicked = await validate_continue_keyboard(user_answer)
    if is_continue_button_clicked or is_all_games_selected:
        await send_age_message()
        await state.set_state(States.age)
        return

    await state.update_data(data)
    await send_choose_games_message(data.get('games'))


@dp.message_handler(state=States.age)
async def process_age(message: types.Message, state: FSMContext):
    user_answer = message.text
    if not is_int(user_answer):
        await send_int_warning()
        return

    age = int(user_answer)
    if not validate_age(age):
        await send_incorrect_age_message()
        return

    if age < WARNING_AGE:
        await send_age_warning()

    await state.update_data(age=age)
    await send_name_message()
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

    await send_country_message()
    await state.set_state(States.country)


@dp.message_handler(state=States.country)
async def process_country(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await validate_countries_keyboard(user_answer):
        await send_incorrect_keyboard_option()
        return

    country_id = await db.get_country_id_by_name(user_answer)
    await state.update_data(country=country_id)

    await send_region_message(country_id)
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

    await send_city_message(region_id)
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

    await send_who_search_message(data.get('age'))
    await state.set_state(States.who_search)


@dp.message_handler(state=States.who_search)
async def process_who_search(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await who_search_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    who_search_id = await who_search_form.get_id_by_text(user_answer)
    await state.update_data(profile_type=who_search_id)
    await send_who_search_next_message_and_state(who_search_id)


@dp.message_handler(state=States.looking_for)
async def process_looking_for(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await who_looking_for_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    who_looking_for_id = await who_looking_for_form.get_id_by_text(user_answer)
    await state.update_data(who_looking_for=who_looking_for_id)

    await send_about_yourself_message()
    await state.set_state(States.about_yourself)


@dp.message_handler(state=States.about_yourself)
async def process_about_yourself(message: types.Message, state: FSMContext):
    await state.update_data(about_yourself=message.text)
    await send_hobby_message()
    await state.set_state(States.hobby)


@dp.message_handler(state=States.hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    await send_photo_message()
    await state.set_state(States.photo)


@dp.message_handler(state=States.photo, content_types=types.ContentTypes.ANY)
async def process_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await send_is_not_a_photo_message()
        return

    await loading_animation()

    photo_link = await get_photo_link(message.photo[-1])
    await state.update_data(photo=photo_link)

    data = await state.get_data()
    data = await unify_data(data, message.from_user.id)
    await show_profile_for_accept(data)
    await state.set_state(States.is_profile_correct)


@dp.message_handler(state=States.is_profile_correct, content_types=types.ContentTypes.ANY)
async def process_is_profile_correct(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id

    if not await confirm_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    data = await state.get_data()
    data = await unify_data(data, user_id)
    await db.update_user(user_id, **data)
    await db.create_profile_if_not_exists_else_update(user_id, **data)

    option_id = await confirm_form.get_id_by_text(user_answer)
    if option_id == confirm_form.yes.id:
        await find_and_show_profile(user_id)
    else:
        await show_user_profile(profile_data=data)


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
        cis_countries_ids = await db.get_cis_countries_ids()
        await state.update_data(search_countries=cis_countries_ids)
        await send_cis_countries_disclaimer_message()
        await send_show_in_random_search_message()
        await state.set_state(States.show_in_random_search)
    # Если пользователь выбрал "Выбрать страну"
    elif teammate_country_type_id == teammate_country_type_form.select_country.id:
        search_countries = []
        await state.update_data(search_countries=search_countries)
        await send_choose_countries_message(search_countries)
        await state.set_state(States.select_countries)
    # Если пользователь выбрал "Любая страна"
    elif teammate_country_type_id == teammate_country_type_form.random_country.id:
        all_countries_ids = await db.get_all_countries_ids()
        await state.update_data(search_countries=all_countries_ids, show_in_random_search=True)
        await send_play_level_message()
        await state.set_state(States.play_level)


@dp.message_handler(state=States.select_countries)
async def process_country_selection(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await validate_select_countries_keyboard(user_answer):
        await send_incorrect_keyboard_option()
        return

    if await validate_continue_keyboard(user_answer):
        await send_show_in_random_search_message()
        await state.set_state(States.show_in_random_search)
        return

    country_id = await db.get_country_id_by_name(user_answer)
    data = await state.get_data()
    data['search_countries'].append(country_id)
    await state.update_data(data)
    await send_choose_countries_message(data.get('search_countries'))


@dp.message_handler(state=States.show_in_random_search)
async def process_show_in_random_search(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await confirm_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    show_in_random_search = await confirm_form.get_id_by_text(user_answer)
    await state.update_data(show_in_random_search=show_in_random_search == confirm_form.yes.id)

    await send_play_level_message()
    await state.set_state(States.play_level)


@dp.message_handler(state=States.play_level)
async def process_play_level(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not await play_level_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    play_level_id = await play_level_form.get_id_by_text(user_answer)
    await state.update_data(play_level=play_level_id)
    await send_call_down_message()
    await state.set_state(States.call_down)


@dp.message_handler(state=States.call_down)
async def process_user_call_down(message: types.Message, state: FSMContext):
    user_answer = message.text

    if not is_float(user_answer):
        await send_float_warning()
        return

    await state.update_data(call_down=float(user_answer))
    await send_about_yourself_message()
    await state.set_state(States.something_about_yourself)


@dp.message_handler(state=States.something_about_yourself)
async def process_something_about_yourself(message: types.Message, state: FSMContext):
    await state.update_data(about_yourself=message.text)
    await send_gamer_photo_message()
    await state.set_state(States.gamer_photo)


@dp.message_handler(state=States.gamer_photo, content_types=types.ContentTypes.ANY)
async def process_gamer_photo(message: types.Message, state: FSMContext):
    photo_link = await get_photo_link(message.photo[-1]) if message.photo else None
    await state.update_data(photo=photo_link)
    await loading_animation()

    data = await state.get_data()
    data = await unify_data(data, message.from_user.id)
    await show_profile_for_accept(data)
    await state.set_state(States.is_profile_correct)


@dp.message_handler(state=States.profile)
async def process_profile(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    data = await state.get_data()

    if not await profile_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    profile_option_id = await profile_form.get_id_by_text(user_answer)
    if profile_option_id == profile_form.edit_profile.id:
        profile_type = data.get('profile_type')
        await send_who_search_next_message_and_state(profile_type)
        await state.reset_data()
        await state.update_data(profile_type=profile_type)
    elif profile_option_id == profile_form.edit_profile_photo.id:
        await send_photo_message()
        await state.set_state(States.edit_photo)
    elif profile_option_id == profile_form.create_profile.id:
        await send_select_profile_message()
        await state.set_state(States.select_profile)
    elif profile_option_id == profile_form.start_searching.id:
        await db.reset_profile_modifications(user_id, data.get('profile_type'))
        await find_and_show_profile(user_id)


@dp.message_handler(state=States.profile_viewing)
async def process_profile_reaction(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id

    if not await profile_viewing_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    user_answer_id = await profile_viewing_form.get_id_by_text(user_answer)
    data = await state.get_data()
    like_author_profile = await db.get_user_profile(user_id, int(data.get('profile_type')))
    if user_answer_id == profile_viewing_form.next.id:
        await find_and_show_profile(user_id)
    elif user_answer_id == profile_viewing_form.like.id:
        user_profile_id = data.get('current_viewing_profile_id')
        await db.like_profile(user_profile_id, like_author_profile.id)

        user = await db.get_profile_user(user_profile_id)
        unseen_profile_likes_count = await db.get_unseen_likes_count(user_profile_id)
        user_state = dp.current_state(user=user.telegram_id, chat=user.telegram_id)
        if unseen_profile_likes_count <= 1:
            await show_your_profile_to_admirer_with_reaction(like_author_profile, user.telegram_id)
            profile = await db.get_profile_by_id(user_profile_id)
            await user_state.update_data(admirer_profile_id=like_author_profile.id, profile_type=profile.type)
        else:
            await send_you_have_likes(user.telegram_id)

        await user_state.set_state(States.admirer_profile_viewing)
        await find_and_show_profile(user_id)
    elif user_answer_id == profile_viewing_form.send_message.id:
        await send_start_message_writing_to_user()
        await state.set_state(States.writing_message_to_another_user)
    elif user_answer_id == profile_viewing_form.sleep.id:
        await send_sleep_message()
        await send_select_profile_message()
        await state.set_state(States.select_profile)


@dp.message_handler(state=States.writing_message_to_another_user)
async def process_message_writing(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_text = message.text

    user = await db.get_profile_user(data.get('current_viewing_profile_id'))
    await send_email_to_another_user(message_text, user.telegram_id)
    await find_and_show_profile(message.from_user.id)


@dp.message_handler(state=States.edit_photo, content_types=types.ContentTypes.ANY)
async def process_edit_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    # If user sent not a photo
    if not message.photo:
        await send_is_not_a_photo_message()
        return

    photo_link = await get_photo_link(message.photo[-1])
    await db.update_profile_photo(user_id, data.get('profile_type'), photo_link)

    await send_profile_photo_was_successfully_edited()
    profile = await db.get_user_profile(user_id, data.get('profile_type'))
    await show_user_profile(profile_id=profile.id)


@dp.message_handler(state=States.answering_to_message)
async def process_answer_to_message(message: types.Message, state: FSMContext):
    user_answer = message.text
    data = await state.get_data()
    await send_answer_to_message(user_answer, data.pop('to_user_message'))
    await send_select_profile_message()
    await state.set_state(States.select_profile)


@dp.message_handler(state=States.reestablish_profile)
async def reestablish_profile_message(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    data = await state.get_data()

    if not await reestablish_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    profile_type = data.get('profile_previewing_type')
    profile = await db.get_user_profile(user_id, profile_type)

    answer_id = await reestablish_form.get_id_by_text(user_answer)
    if answer_id == reestablish_form.reestablish.id:
        await show_user_profile(profile_id=profile.id)
    elif answer_id == reestablish_form.delete.id:
        await db.delete_profile(profile.id)
        await start_full_profile_creation()


@dp.message_handler(state=States.choose_profiles_to_reestablish)
async def process_profile_choosing_to_reestablish(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id

    if not await reestablish_many_from.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    user_answer_id = await reestablish_many_from.get_id_by_text(user_answer)
    if user_answer_id == reestablish_many_from.all.id:
        await send_select_profile_message()
        await state.set_state(States.select_profile)
    elif user_answer_id == reestablish_many_from.choose.id:
        await ask_profile_num_to_reestablish()
        await state.set_state(States.reestablish_profile_by_num)
    elif user_answer_id == reestablish_many_from.delete_all.id:
        await db.delete_all_user_profiles(user_id)
        await start_full_profile_creation()


@dp.message_handler(state=States.reestablish_profile_by_num)
async def process_profile_num_to_reestablish(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id

    if not is_int(user_answer):
        await send_int_warning()
        return

    profile_num = int(user_answer)
    user_profiles = await db.get_all_user_active_profiles(user_id)
    if profile_num > len(user_profiles):
        await send_incorrect_profile_num()
        return

    await db.delete_profiles_with_exception(user_id, profile_num)
    profile = await db.get_user_profile(user_id, profile_num)
    await show_user_profile(profile_id=profile.id)


@dp.message_handler(state=States.search_modification)
async def process_data_modification(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id

    if not await edit_search_modification_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    modifications = None
    field_id = await edit_search_modification_form.get_id_by_text(user_answer)
    if field_id == edit_search_modification_form.set_target_gender.id:
        modifications = ModificationTypes.GENDER
    elif field_id == edit_search_modification_form.set_target_games.id:
        modifications = ModificationTypes.GAMES

    data = await state.get_data()
    await db.update_profile_modifications(user_id, data.get('profile_type'), modifications)
    await find_and_show_profile(user_id)


@dp.message_handler(state=States.admirer_profile_viewing)
async def process_admirer_profile_viewing(message: types.Message, state: FSMContext):
    user_answer = message.text
    data = await state.get_data()

    if not await admirer_profile_viewing_form.validate_message(user_answer):
        await send_incorrect_keyboard_option()
        return

    user = await db.get_user_by_telegram_id(message.from_user.id)
    user_profile = await db.get_user_profile(user.telegram_id, data.get('profile_type'))

    admirer_profile_id = int(data.get('admirer_profile_id'))
    await db.like_is_seen(user_profile.id, admirer_profile_id)

    option_id = await admirer_profile_viewing_form.get_id_by_text(user_answer)
    if option_id == admirer_profile_viewing_form.like.id:
        admirer_user = await db.get_profile_user(admirer_profile_id)
        await send_you_have_mutual_sympathy_message(user, admirer_user.telegram_id)
        await show_your_profile_to_another_user(user_profile, admirer_user.telegram_id)
        await send_message_with_admirer_telegram_link(admirer_user)
    elif option_id in (admirer_profile_viewing_form.next.id, admirer_profile_viewing_form.sleep.id):
        data.pop('admirer_profile_id', None)
        await delete_keyboard(message)
    elif option_id == admirer_profile_viewing_form.complain.id:
        await state.update_data(complain_profile_id=admirer_profile_id)
        await send_select_complain_type_form()
        await state.set_state(States.choose_complain_type)
        return

    unseen_likes_count = await db.get_unseen_likes_count(user_profile.id)
    if unseen_likes_count >= 1:
        next_unseen_profile = await db.get_next_unseen_profile_like(user_profile.id)
        if next_unseen_profile:
            next_unseen_profile_id = next_unseen_profile.who_liked_profile_id
            profile = await db.get_profile_by_id(next_unseen_profile_id)
            await show_admirer_profile(profile)
            await state.update_data(admirer_profile_id=next_unseen_profile_id)
            return

    await state.update_data(data)
    await send_select_profile_message()
    await state.set_state(States.select_profile)
