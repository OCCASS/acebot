from loader import db, _


async def validate(answer_option: list, user_answer: str) -> bool:
    for option in answer_option:
        if user_answer == _(option):
            return True
    else:
        return False


async def validate_good_keyboard(user_answer: str) -> bool:
    return await validate(['Хорошо'], user_answer)


async def validate_continue_keyboard(user_answer: str) -> bool:
    return await validate(['Продолжить'], user_answer)


async def validate_games_keyboard(user_answer: str) -> bool:
    all_games = await db.get_all_games()
    all_games_name_list = [game.name for game in all_games]
    all_options = all_games_name_list + ['Продолжить']
    return await validate(all_options, user_answer)


async def validate_countries_keyboard(user_answer: str) -> bool:
    all_countries = await db.get_all_countries()
    all_country_names = [country.name for country in all_countries]

    return await validate(all_country_names, user_answer)


async def validate_regions_keyboard(user_answer: str, country_id: int) -> bool:
    all_regions = await db.get_regions_by_country(country_id)
    all_regions_names = [region.name for region in all_regions]

    return await validate(all_regions_names, user_answer)


async def validate_cities_keyboard(user_answer: str, region_id: int) -> bool:
    all_cities = await db.get_cities_by_region(region_id)
    all_city_names = [city.name for city in all_cities]

    return await validate(all_city_names, user_answer)
