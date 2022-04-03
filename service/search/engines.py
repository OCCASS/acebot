from data.types import WhoLookingForTypes, GenderTypes
from service.search._base import BaseSearchEngine
from service.search._constants import ALL_GENDERS
from service.search._types import GeographicalPosition, Accuracy


class SearchPeopleIRLEngine(BaseSearchEngine):
    async def _get_another_user_geographical_position(self, user):
        return user.city

    async def _get_geographical_position(self) -> GeographicalPosition:
        return self._user.city

    async def _get_genders(self):
        additional = self._profile.additional
        who_looking_for_type = additional.get('who_looking_for')
        if who_looking_for_type == WhoLookingForTypes.GUYS:
            return [GenderTypes.GUY]
        elif who_looking_for_type == WhoLookingForTypes.GIRLS:
            return [GenderTypes.GIRL]
        else:
            return [GenderTypes.GUY, GenderTypes.GIRL]

    async def _get_age_accuracy(self, age: int) -> Accuracy:
        if age < 14:
            return Accuracy(1, 0)
        elif 14 <= age <= 22:
            return Accuracy(2, 2)
        else:
            return Accuracy(5, 5)


class SearchJustPlayEngine(BaseSearchEngine):
    async def _get_another_user_geographical_position(self, user):
        return await user.get_country()

    async def _get_geographical_position(self) -> GeographicalPosition:
        return await self._user.get_country()

    async def _get_genders(self):
        return ALL_GENDERS

    async def _get_age_accuracy(self, age: int) -> Accuracy:
        if age < 14:
            return Accuracy(1, 0)
        elif 14 <= age < 20:
            return Accuracy(2, 2)
        else:
            return Accuracy(40, 2)
