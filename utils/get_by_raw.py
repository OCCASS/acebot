from loader import _, db
from service.database.api import DatabaseApi


async def get_country_id(raw_country: str):
    for country in await db.get_all_countries():
        if _(country.name) == raw_country:
            return country.id


async def get_city_id(raw_city: str, country_id: int):
    for city in await db.get_cities_by_country(country_id):
        if _(city.name) == raw_city:
            return city.id
