import datetime
from typing import List

from sqlalchemy import and_

from data.config import CIS_COUNTRIES, DAYS_IN_MONTH, DEFAULT_LOCALE
from data.types import BanDurationTypes
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

    async def update_user_username(self, user_telegram_id: int, username: str):
        user = await self.get_user_by_telegram_id(user_telegram_id)
        await user.update(username=username).apply()

    @staticmethod
    async def get_all_users():
        return await User.query.gino.all()

    @staticmethod
    async def create_user(telegram_id: int, name: str, username: str):
        await User.create(telegram_id=telegram_id, name=name, username=username)

    async def update_user(
            self, telegram_id: int, *, name: str, gender: int, age: int, games: list, cities: list,
            **kwargs):
        user = await self.get_user_by_telegram_id(telegram_id)
        await user.update(gender=gender, age=age, games=games, name=name, cities=cities).apply()

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
        profile = await Profile.query.where(
            and_(Profile.user_id == user.id, Profile.type == profile_type, Profile.enable)).gino.first()
        return True if profile else False

    @staticmethod
    async def create_profile(
            user_id: int, photo: str, profile_type: int, description: str,
            additional: Json, enable: bool):
        created_at = datetime.datetime.now()
        await Profile.create(user_id=user_id, photo=photo, type=profile_type, description=description,
                             additional=additional, modified_at=created_at, enable=enable)

    async def update_profile(
            self, user_id: int, photo: str, profile_type: int, description: str,
            additional: Json, enable: bool):
        profile = await Profile.query.where(and_(Profile.user_id == user_id, Profile.type == profile_type)).gino.first()

        is_search_parameters_edited = profile.additional != additional
        if is_search_parameters_edited:
            await self.drop_last_seen_profile_id(profile.id)

        modified_at = datetime.datetime.now()
        await profile.update(photo=photo, description=description, additional=additional,
                             type=profile_type, modified_at=modified_at, enable=enable).apply()

    async def create_profile_if_not_exists_else_update(
            self, user_telegram_id: int, *, profile_type: int, photo: str,
            description: str, additional: Json, **kwargs):
        user = await self.get_user_by_telegram_id(user_telegram_id)
        profile_created = await self.is_profile_created(user, profile_type)
        enable = True
        if profile_created:
            await self.update_profile(user.id, photo, profile_type, description, additional, enable)
        else:
            await self.create_profile(user.id, photo, profile_type, description, additional, enable)

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
        return await Country.query.order_by(Country.name).gino.all()

    async def get_all_countries_by_locale(self, locale=None):
        if locale is None:
            locale = DEFAULT_LOCALE

        async with db.acquire() as conn:
            cities = await db.status(db.text(
                "SELECT names -> :locale FROM country",
            ), {'locale': locale})

        return list(filter(lambda x: x is not None, map(lambda x: x[0], cities[1])))

    async def get_all_cities_by_locale_and_country(self, country_id, locale=None):
        if locale is None:
            locale = DEFAULT_LOCALE

        async with db.acquire() as conn:
            cities = await db.status(db.text(
                "SELECT names -> :locale FROM city WHERE country_id=:country_id",
            ), {'locale': locale, 'country_id': country_id})

        return list(filter(lambda x: x is not None, map(lambda x: x[0], cities[1])))

    @staticmethod
    async def get_cities_by_country(country_id: int):
        return await City.query.where(City.country_id == country_id).gino.all()

    @staticmethod
    async def get_country_id_by_name(name: str):
        country = await Country.query.where(Country.name == name).gino.first()
        return country.id

    async def get_country_id_by_name_and_locale(self, name, locale):
        async with db.acquire() as conn:
            countries = await db.status(db.text(
                "SELECT id FROM country WHERE names ->> :locale = :name LIMIT 1",
            ), {'locale': locale, 'name': name})

        return countries[1][0][0]

    async def get_city_id_by_name_and_locale(self, name, locale):
        async with db.acquire() as conn:
            cities = await db.status(db.text(
                "SELECT id FROM city WHERE names ->> :locale = :name LIMIT 1",
            ), {'locale': locale, 'name': name})

        if cities[1]:
            return cities[1][0][0]

        return None

    async def get_city_name_by_id_and_locale(self, city_id, locale):
        city = await self.get_city_by_id(city_id)
        return city.get(locale)

    @staticmethod
    async def get_city_id_by_name(name: str):
        city = await City.query.where(City.name == name).gino.first()
        return city.id

    @staticmethod
    async def get_country_by_id(id_: int):
        return await Country.query.where(Country.id == id_).gino.first()

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

    @staticmethod
    async def like_profile(liked_profile_id: int, who_liked_profile_id: int, message: Union[str, None] = None) -> None:
        like = await Like.query.where(
            and_(Like.liked_profile_id == liked_profile_id,
                 Like.who_liked_profile_id == who_liked_profile_id)).gino.first()
        if like is None or like.is_like_seen:
            await Like.create(liked_profile_id=liked_profile_id, who_liked_profile_id=who_liked_profile_id,
                              message=message)

    @staticmethod
    async def like_is_seen(who_seen_profile_id: int, who_liked_profile_id: int) -> None:
        like = await Like.query.where(
            and_(Like.who_liked_profile_id == who_liked_profile_id,
                 Like.liked_profile_id == who_seen_profile_id)).gino.first()
        await like.update(is_like_seen=True).apply()

    @staticmethod
    async def get_unseen_likes_count(profile_id: int) -> int:
        likes = await Like.query.where(and_(Like.liked_profile_id == profile_id, Like.is_like_seen == False)).gino.all()
        return len(likes)

    @staticmethod
    async def get_next_unseen_profile_like(profile_id: int) -> Like:
        like = await Like.query.where(
            and_(Like.liked_profile_id == profile_id, Like.is_like_seen == False)).gino.first()
        return like

    async def drop_last_seen_profile_id(self, profile_id: int):
        profile = await self.get_profile_by_id(profile_id)
        await profile.update(last_seen_profile_id=None).apply()

    @staticmethod
    async def create_complain(to_profile_id: int, from_profile_id: int, complain_type: int):
        sent_at = datetime.datetime.now()
        await Complain.create(to_profile_id=to_profile_id, from_profile_id=from_profile_id, complain_type=complain_type,
                              sent_at=sent_at)

    @staticmethod
    async def get_profile_complains_count(profile_id: int):
        complains = await Complain.query.where(Complain.to_profile_id == profile_id).gino.all()
        return len(complains)

    async def create_ban(self, to_user_telegram_id: int, ban_type: int):
        from_datetime = datetime.datetime.now()
        user = await self.get_user_by_telegram_id(to_user_telegram_id)
        await Ban.create(to_user_id=user.id, from_date=from_datetime, type=ban_type)

    @staticmethod
    async def get_profile_complains(profile_id: int):
        return await Complain.query.where(Complain.to_profile_id == profile_id).gino.all()

    async def delete_all_profile_complains(self, profile_id: int):
        for complain in await self.get_profile_complains(profile_id):
            await complain.delete()

    async def is_user_banned(self, user_telegram_id: int):
        ban = await self.get_user_ban(user_telegram_id)
        return True if ban else False

    @staticmethod
    async def get_all_users_bans():
        return await Ban.query.gino.all()

    @staticmethod
    async def get_ban_duration(ban: Ban):
        if ban.type == BanDurationTypes.ONE_DAY:
            return datetime.timedelta(days=1)
        elif ban.type == BanDurationTypes.ONE_MONTH:
            return datetime.timedelta(days=DAYS_IN_MONTH)
        elif ban.type == BanDurationTypes.FOREVER:
            return

    async def get_user_ban(self, user_telegram_id: int):
        user = await self.get_user_by_telegram_id(user_telegram_id)
        if user:
            return await Ban.query.where(Ban.to_user_id == user.id).gino.first()
        else:
            return False

    async def get_user_ban_end_datetime(self, user_telegram_id: int) -> Union[datetime.datetime, None]:
        ban = await self.get_user_ban(user_telegram_id)
        ban_duration = await self.get_ban_duration(ban)
        if ban_duration is not None:
            return ban.from_date + ban_duration
        else:
            return

    async def create_country(self, names):
        return await Country.create(
            names=names
        )

    async def update_country_names(self, country_id, names):
        country = await self.get_country_by_id(country_id)
        await country.update(names=names).apply()
        return country

    async def create_city(self, names, country_id):
        return await City.create(
            country_id=country_id,
            names=names
        )

    async def update_city_names(self, city_id, names):
        city = await self.get_city_by_id(city_id)
        await city.update(names=names).apply()
        return city
