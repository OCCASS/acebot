from data.types import ModificationTypes
from loader import db
from .constants import ALL_GENDERS
from ._types import ProfileType, Gender, AgeRange, GeographicalPosition, Accuracy
from typing import Union, List
from service.database.models import Profile
from sqlalchemy import and_


class InlineFunction:
    def __init__(self, return_value):
        self._return_value = return_value

    def __call__(self, *args, **kwargs):
        return self._return_value


class BaseSearchEngine:
    def __init__(self, user_telegram_id: int, profile_type: ProfileType):
        self._user_telegram_id = user_telegram_id
        self._profile_type = profile_type

        self._last_seen_profile_id = None
        self.user = None
        self.profile = None

    async def init(self) -> None:
        await self._get_user()
        await self._get_last_seen_profile_id()

    async def _get_last_seen_profile_id(self):
        self._last_seen_profile_id = await db.get_user_last_seen_profile_id(self._user_telegram_id)
        self._last_seen_profile_id = self._last_seen_profile_id or 0

    async def get_profiles(self) -> List[Profile]:
        return await Profile.query.where(and_(
            Profile.type == self._profile_type,
            Profile.id > self._last_seen_profile_id,
            Profile.user_id != self.user.id
        )).gino.all()

    async def search(self):
        profiles = await self.get_profiles()
        for profile in profiles:
            properties = (
                self._check_age(),
                self._check_gender(),
                self._check_geographical_position(profile),
                self.check_games(profile),
                self.check_another_properties(profile),
            )
            if all(properties):
                return profile

        return

    async def _get_user(self) -> None:
        self.user = await db.get_user_by_telegram_id(self._user_telegram_id)

    async def _get_profile(self) -> None:
        self.profile = await db.get_user_profile(self._user_telegram_id, self._profile_type)

    def _get_gender(self) -> Gender:
        return self.user.gender

    def _get_age(self) -> int:
        return self.user.age

    @staticmethod
    def ignore() -> bool:
        """
        Это функций заглушка, если метод не надо использовать для проверки,
        надо просто присвоить ему ignore и тогда он вернет True
        """

        return True

    async def _check_geographical_position(self, profile: Profile) -> bool:
        current_gp = await self.get_geographical_position()
        another_user = await db.get_profile_user(profile.id)
        another_user_gp = await self.get_another_user_geographical_position(another_user)
        return current_gp == another_user_gp

    async def _check_gender(self) -> bool:
        modification_type = self.profile.modification_type

        if modification_type == ModificationTypes.GENDER:
            return True

        gender = self._get_gender()
        genders = await self.get_genders()

        if genders == ALL_GENDERS:
            return True

        return gender in genders

    def _get_age_range(self) -> AgeRange:
        age = self._get_age()
        accuracy = self.get_age_accuracy(age)
        return AgeRange(age - accuracy.back, age + accuracy.forward)

    async def _check_age(self):
        age = self._get_age()
        age_range = self._get_age_range()
        return age_range.start <= age <= age_range.end

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

    def check_another_properties(self, another_profile: Profile) -> bool:
        return self.ignore()
