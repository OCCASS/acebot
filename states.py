from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    language = State()
    introduction = State()
    introduction1 = State()
    select_games = State()
    age = State()
    who_search = State()
    gender = State()
    looking_for = State()
    country = State()

    city = State()
    is_city_correctly_determined = State()
    add_more_cities = State()
    retry_city = State()
    new_city_language = State()
    new_city_name = State()

    name = State()
    about_yourself = State()
    hobby = State()
    photo = State()
    is_profile_correct = State()
    profile = State()
    teammate_country_type = State()
    show_in_random_search = State()
    select_countries = State()
    play_level = State()
    call_down = State()
    something_about_yourself = State()
    gamer_photo = State()
    select_profile = State()
    edit_photo = State()
    profile_viewing = State()
    writing_message_to_another_user = State()
    answering_to_message = State()
    search_modification = State()
    view_created_accounts = State()
    reestablish_profile = State()
    choose_profiles_to_reestablish = State()
    reestablish_profile_by_num = State()
    admirer_profile_viewing = State()
    choose_complain_type = State()
    intruder_ban_duration = State()
    message_to_subs = State()

    new_country_language = State()
    new_country_name = State()
