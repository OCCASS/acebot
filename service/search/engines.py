from data.types import WhoLookingForTypes, GenderTypes, ModificationTypes
from service.database.models import Profile
from service.search._base import BaseSearchEngine
from service.search.constants import ALL_GENDERS
from service.search._types import GeographicalPosition, Accuracy
from loader import db


class SearchPeopleIRLEngine(BaseSearchEngine):
    async def get_another_user_geographical_position(self, user):
        return user.cities

    async def get_geographical_position(self) -> GeographicalPosition:
        return self.user.cities

    async def get_genders(self):
        additional = self.profile.additional
        who_looking_for_type = int(additional.get('who_looking_for'))
        if who_looking_for_type == WhoLookingForTypes.GUYS:
            return [GenderTypes.GUY]
        elif who_looking_for_type == WhoLookingForTypes.GIRLS:
            return [GenderTypes.GIRL]
        else:
            return [GenderTypes.GUY, GenderTypes.GIRL]

    def get_age_accuracy(self, age: int) -> Accuracy:
        if age < 14:
            return Accuracy(1, 0)
        elif 14 <= age <= 22:
            return Accuracy(2, 2)
        else:
            return Accuracy(5, 5)

    async def check_games(self, another_profile: Profile):
        return self.ignore()


class SearchJustPlayEngine(BaseSearchEngine):
    async def get_another_user_geographical_position(self, user):
        return await user.get_countries()

    async def get_geographical_position(self) -> GeographicalPosition:
        return await self.user.get_countries()

    async def get_genders(self):
        return ALL_GENDERS

    def get_age_accuracy(self, age: int) -> Accuracy:
        if age < 14:
            return Accuracy(1, 0)
        elif 14 <= age < 20:
            return Accuracy(2, 2)
        else:
            return Accuracy(40, 2)

    async def check_games(self, another_profile: Profile) -> bool:
        if self.profile.modification_type == ModificationTypes.GAMES:
            return True

        another_user = await db.get_profile_user(another_profile.id)
        if len(set(self.user.games) & set(another_user.games)) > 0:
            return True

        return False
