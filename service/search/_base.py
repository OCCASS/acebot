import datetime
from typing import Union, List

from sqlalchemy import and_

from data.config import DAYS_IN_MONTH
from data.types import ModificationTypes
from loader import db
from service.database.models import Profile
from ._types import ProfileType, Gender, AgeRange, GeographicalPosition, Accuracy
from .constants import ALL_GENDERS


class BaseSearchEngine:
    def __init__(self, user_telegram_id: int, profile_type: ProfileType):
        self._user_telegram_id = user_telegram_id
        self._profile_type = profile_type

        self.user = None
        self.profile = None

    async def init(self) -> None:
        await self._get_user()
        await self._get_profile()

    async def get_profiles(self) -> List[Profile]:
        profiles = await Profile.query.where(
            and_(
                Profile.type == self.profile.type,
                Profile.user_id != self.user.id,
                Profile.enable,
            )
        ).order_by(Profile.id).gino.all()
        return profiles

    async def search(self):
        profiles = await self.get_profiles()
        for profile in profiles:
            properties = (
                self._check_age(),
                await self._check_gender(profile),
                await self._check_geographical_position(profile),
                await self.check_games(profile),
                await self.check_another_properties(profile),
            )
            additional_properties = (
                await self._check_is_profile_seen_one_month_ago(profile),
                await self._check_is_profile_seen_after_modification(profile),
            )
            if all(properties):
                if not await self._is_profile_seen(profile):
                    return profile
                else:
                    if any(additional_properties):
                        return profile

        return

    async def _get_user(self) -> None:
        self.user = await db.get_user_by_telegram_id(self._user_telegram_id)

    async def _get_profile(self) -> None:
        self.profile = await db.get_user_profile(self._user_telegram_id, self._profile_type)

    def _get_gender(self) -> Gender:
        return self.user.gender

    def _get_age(self) -> int:
        return int(self.user.age)

    @staticmethod
    def ignore() -> bool:
        """
        Это функций заглушка, если метод не надо использовать для проверки,
        надо просто присвоить ему ignore и тогда он вернет True
        """

        return True

    async def _is_profile_seen(self, profile):
        return profile.id <= (self.profile.last_seen_profile_id or 0)

    async def _check_geographical_position(self, profile: Profile) -> bool:
        current_gp = await self.get_geographical_position()
        another_user = await db.get_profile_user(profile.id)
        another_user_gp = await self.get_another_user_geographical_position(another_user)
        return current_gp == another_user_gp

    async def _check_gender(self, profile) -> bool:
        modification_type = self.profile.modification_type
        if modification_type == ModificationTypes.GENDER:
            return True

        user = await db.get_profile_user(profile.id)
        gender = user.gender
        genders = await self.get_genders()

        if genders == ALL_GENDERS:
            return True

        return gender in genders

    def _get_age_range(self) -> AgeRange:
        age = self._get_age()
        accuracy = self.get_age_accuracy(age)
        return AgeRange(age - accuracy.back, age + accuracy.forward)

    def _check_age(self):
        age = self._get_age()
        age_range = self._get_age_range()
        return age_range.start <= age <= age_range.end

    async def _check_is_profile_seen_one_month_ago(self, profile) -> bool:
        now_datetime = datetime.datetime.now()
        seen_profile = await db.get_seen_profile_or_none(self.profile.id, profile.id)
        if seen_profile:
            # if (now_datetime - seen_profile.seen_at).days >= DAYS_IN_MONTH:
            if (now_datetime - seen_profile.seen_at).total_seconds() >= 60 * 60 * 60:
                return True
            else:
                return False

        return True

    async def _check_is_profile_seen_after_modification(self, profile) -> bool:
        seen_profile = await db.get_seen_profile_or_none(self.profile.id, profile.id)
        if seen_profile:
            return profile.modified_at > seen_profile.seen_at

        return True

    async def get_geographical_position(self) -> GeographicalPosition:
        raise NotImplementedError

    def get_age_accuracy(self, age: int) -> Accuracy:
        raise NotImplementedError

    async def get_another_user_geographical_position(self, user):
        raise NotImplementedError

    async def get_genders(self) -> Union[List[Gender], int]:
        raise NotImplementedError

    async def check_games(self, another_profile: Profile):
        raise NotImplementedError

    async def check_another_properties(self, another_profile: Profile) -> bool:
        return self.ignore()
