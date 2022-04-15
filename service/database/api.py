import datetime
from typing import List

from sqlalchemy import and_

from data.config import CIS_COUNTRIES
from .models import *
from ._types import Json


class DatabaseApi:
    @staticmethod
    async def get_user_by_telegram_id(user_telegram_id: int):
        return await User.query.where(User.telegram_id == user_telegram_id).gino.first()

    @staticmethod
    async def get_user_by_id(user_id: int):
        return await User.query.where(User.id == user_id).gino.first()

    async def set_user_locale(self, user_telegram_id: int, new_locale: str):
        user = await self.get_user_by_telegram_id(user_telegram_id)
        await user.update(locale=new_locale).apply()

    @staticmethod
    async def create_user(telegram_id: int, name: str, username: str):
        await User.create(telegram_id=telegram_id, name=name, username=username)

    async def update_user(self, telegram_id: int, *, name: str, gender: int, age: int, games: list, city: int,
                          **kwargs):
        user = await self.get_user_by_telegram_id(telegram_id)
        await user.update(gender=gender, age=age, games=games, name=name, city=city).apply()

    @staticmethod
    async def get_all_user_active_profiles(user_telegram_id: int) -> Union[List[Profile], None]:
        user = await User.query.where(User.telegram_id == user_telegram_id).gino.first()

        if not user:
            return

        profiles = await Profile.query.where(and_(Profile.user_id == user.id, Profile.enable)).order_by(
            Profile.type).gino.all()
        return profiles

    async def get_user_profile(self, user_telegram_id: int, profile_type: int):
        user = await self.get_user_by_telegram_id(user_telegram_id)
        return await Profile.query.where(
            and_(Profile.user_id == user.id, Profile.type == profile_type, Profile.enable)).gino.first()

    @staticmethod
    async def get_profile_by_id(profile_id: int):
        return await Profile.query.where(Profile.id == profile_id).gino.first()

    async def get_profile_user(self, profile_id: int):
        profile = await self.get_profile_by_id(profile_id)
        return await User.query.where(User.id == profile.user_id).gino.first()

    async def update_last_seen_profile_id(self, profile_id, new_value: int):
        profile = await self.get_profile_by_id(profile_id)
        await profile.update(last_seen_profile_id=new_value).apply()

    async def update_profile_photo(self, user_telegram_id: int, profile_type: int, photo: str):
        user = await self.get_user_by_telegram_id(user_telegram_id)
        profile = await Profile.query.where(
            and_(Profile.user_id == user.id, Profile.type == int(profile_type))).gino.first()
        await profile.update(photo=photo).apply()

    @staticmethod
    async def is_profile_created(user: User, profile_type: int) -> bool:
        profile = await Profile.query.where(and_(Profile.user_id == user.id, Profile.type == profile_type)).gino.first()
        return True if profile else False

    @staticmethod
    async def create_profile(user_id: int, photo: str, profile_type: int, description: str,
                             additional: Json):
        created_at = datetime.datetime.now()
        await Profile.create(user_id=user_id, photo=photo, type=profile_type, description=description,
                             additional=additional, modified_at=created_at)

    @staticmethod
    async def update_profile(user_id: int, photo: str, profile_type: int, description: str,
                             additional: Json):
        profile = await Profile.query.where(and_(Profile.user_id == user_id, Profile.type == profile_type)).gino.first()
        modified_at = datetime.datetime.now()
        await profile.update(photo=photo, description=description, additional=additional,
                             type=profile_type, modified_at=modified_at).apply()

    async def create_profile_if_not_exists_else_update(self, user_telegram_id: int, *, profile_type: int, photo: str,
                                                       description: str, additional: Json, **kwargs):
        user = await self.get_user_by_telegram_id(user_telegram_id)
        profile_created = await self.is_profile_created(user, profile_type)
        if profile_created:
            await self.update_profile(user.id, photo, profile_type, description, additional)
        else:
            await self.create_profile(user.id, photo, profile_type, description, additional)

    @staticmethod
    async def get_all_games() -> list:
        return await Game.query.gino.all()

    @staticmethod
    async def get_game_by_id(game_id: int):
        return await Game.query.where(Game.id == game_id).gino.first()

    @staticmethod
    async def get_game_by_name(name: str) -> Game:
        return await Game.query.where(Game.name == name).gino.first()

    @staticmethod
    async def is_user_exists(telegram_id: int):
        user = await User.query.where(User.telegram_id == telegram_id).gino.first()
        return True if user else False

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
    async def get_country_by_id(id_: int):
        return await Country.query.where(Country.id == id_).gino.first()

    @staticmethod
    async def get_region_by_id(id_: int):
        return await Region.query.where(Region.id == id_).gino.first()

    @staticmethod
    async def get_city_by_id(id_: int):
        return await City.query.where(City.id == id_).gino.first()

    async def get_cis_countries(self):
        all_countries = await self.get_all_countries()
        cis_countries = [country for country in all_countries if country.name in CIS_COUNTRIES]
        return cis_countries

    async def get_cis_countries_ids(self):
        cis_countries = await self.get_cis_countries()
        return [country.id for country in cis_countries]

    async def get_all_countries_ids(self):
        all_countries = await self.get_all_countries()
        return [country.id for country in all_countries]

    async def update_profile_modifications(self, user_telegram_id: int, profile_type: int, modifications: int):
        profile = await self.get_user_profile(user_telegram_id, profile_type)
        await profile.update(modification_type=modifications).apply()

    async def reset_profile_modifications(self, user_telegram_id: int, profile_type: int):
        profile = await self.get_user_profile(user_telegram_id, profile_type)
        if profile:
            await profile.update(modification_type=None).apply()

    async def delete_all_user_profiles(self, user_telegram_id: int):
        user_profiles = await self.get_all_user_active_profiles(user_telegram_id)
        for profile in user_profiles:
            await self.delete_profile(profile.id)

    async def delete_profile(self, profile_id):
        profile = await self.get_profile_by_id(profile_id)
        await profile.update(enable=False).apply()

    async def delete_profiles_with_exception(self, user_telegram_id: int, exception: int):
        all_profiles = await self.get_all_user_active_profiles(user_telegram_id)
        for profile in all_profiles:
            if profile.type == exception:
                continue

            await profile.update(enable=False).apply()

    @staticmethod
    async def get_seen_profile_or_none(who_saw_profile_id, who_seen_profile_id):
        return await SeenProfiles.query.where(
            and_(
                SeenProfiles.who_saw_profile_id == who_saw_profile_id,
                SeenProfiles.who_seen_profile_id == who_seen_profile_id
            )
        ).gino.first()

    async def add_or_update_seen_profile(self, who_saw_profile_id, who_seen_profile_id):
        seen_at = datetime.datetime.now()
        profile = await self.get_seen_profile_or_none(who_saw_profile_id, who_seen_profile_id)
        if profile:
            await profile.update(seen_at=seen_at).apply()
        else:
            await SeenProfiles.create(who_saw_profile_id=who_saw_profile_id, seen_at=seen_at,
                                      who_seen_profile_id=who_seen_profile_id)

    async def like_profile(self, who_like, who_liked):
        profile_in_seen = await self.get_seen_profile_or_none(who_like, who_liked)
        await profile_in_seen.update(liked=True).apply()
