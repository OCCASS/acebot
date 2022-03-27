from typing import Union

from .models import *


class DatabaseApi:
    @staticmethod
    async def get_user(user_telegram_id: int):
        user = await User.query.where(User.telegram_id == user_telegram_id).gino.first()
        return user

    async def set_user_locale(self, user_telegram_id: int, new_locale: str):
        user = await self.get_user(user_telegram_id)
        await user.update(locale=new_locale).apply()

    @staticmethod
    async def get_all_games() -> list:
        return await Game.query.gino.all()

    @staticmethod
    async def get_game_by_name(name: str) -> Game:
        return await Game.query.where(Game.name == name).gino.first()

    @staticmethod
    async def is_user_exists(telegram_id: int):
        user = await User.query.where(User.telegram_id == telegram_id).gino.first()
        return True if user else False

    @staticmethod
    async def create_user(telegram_id: int, name: str, username: str):
        await User.create(telegram_id=telegram_id, name=name, username=username)

    async def update_user(self, telegram_id: int, name: str, gender: int, city: int, age: int, games: list):
        user = await self.get_user(telegram_id)
        await user.update(gender=gender, city=city, age=age, games=games, name=name).apply()

    @staticmethod
    async def get_all_genders() -> list:
        return await Gender.query.gino.all()

    @staticmethod
    async def get_gender_by_name(name: str):
        return await Gender.query.where(Gender.name == name).gino.first()

    @staticmethod
    async def get_all_countries():
        return await Country.query.gino.all()

    @staticmethod
    async def get_regions_by_country(country_id: int):
        return await Region.query.where(Region.country_id == country_id).gino.all()

    @staticmethod
    async def get_cities_by_region(region_id: int):
        return await City.query.where(City.region_id == region_id).gino.all()

    @staticmethod
    async def get_country_id_by_name(name: str):
        country = await Country.query.where(Country.name == name).gino.first()
        return country.id

    @staticmethod
    async def get_region_id_by_name(name: str):
        region = await Region.query.where(Region.name == name).gino.first()
        return region.id

    @staticmethod
    async def get_city_id_by_name(name: str):
        city = await City.query.where(City.name == name).gino.first()
        return city.id

    @staticmethod
    async def get_game_by_id(game_id: int):
        return await Game.query.where(Game.id == game_id).gino.first()

    @staticmethod
    async def get_country_by_id(id_: int):
        return await Country.query.where(Country.id == id_).gino.first()

    @staticmethod
    async def get_region_by_id(id_: int):
        return await Region.query.where(Region.id == id_).gino.first()

    @staticmethod
    async def get_city_by_id(id_: int):
        return await City.query.where(City.id == id_).gino.first()

    @staticmethod
    async def is_profile_created(user: User, profile_type: int) -> bool:
        profile = await Profile.query.where(Profile.user_id == user.id, Profile.type == profile_type).gino.first()
        return True if profile else False

    @staticmethod
    async def create_profile(user_id: int, photo: str, profile_type: int, description: str,
                             additional: Union[dict, list]):
        await Profile.create(user_id=user_id, photo=photo, type=profile_type, description=description,
                             additional=additional)

    @staticmethod
    async def update_profile(user_id: int, photo: str, profile_type: int, description: str,
                             additional: Union[dict, list]):
        profile = Profile.query.where(Profile.user_id == user_id, Profile.type == profile_type)
        await profile.update(photo=photo, description=description, additional=additional).apply()

    async def create_profile_if_not_exists_else_update(self, user_telegram_id: int, *, profile_type: int, photo: str,
                                                       description: str, additional: Union[dict, list]):
        user = await self.get_user(user_telegram_id)
        profile_created = await self.is_profile_created(user, profile_type)
        if profile_created:
            await self.update_profile(user.id, photo, profile_type, description, additional)
        else:
            await self.create_profile(user.id, photo, profile_type, description, additional)
