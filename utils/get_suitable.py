from loader import db
from fuzzywuzzy import fuzz


async def get_suitable_country(raw_text: str):
    all_countries = await db.get_all_countries()
    percent_country_id_pairs = []
    raw_text = raw_text.lower()
    for country in all_countries:
        percent = fuzz.partial_ratio(raw_text, country.name.lower())
        percent_country_id_pairs.append((percent, country))

    return list(sorted(percent_country_id_pairs, key=lambda x: x[0], reverse=True))[0]


async def get_suitable_city(country_id: int, raw_text: str):
    all_cities = await db.get_cities_by_country(country_id)
    percent_city_id_pairs = []
    raw_text = raw_text.lower()
    for city in all_cities:
        percent = fuzz.partial_ratio(raw_text, city.name.lower(i))
        percent_city_id_pairs.append((percent, city))

    return list(sorted(percent_city_id_pairs, key=lambda x: x[0], reverse=True))[0]
