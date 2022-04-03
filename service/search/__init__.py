from typing import Union

from data.types import ProfileTypes
from service.database.models import Profile
from service.search.engines import SearchPeopleIRLEngine, SearchJustPlayEngine

SEARCH_ENGINES = {
    ProfileTypes.PERSON_IRL: SearchPeopleIRLEngine,
    ProfileTypes.JUST_PLAY: SearchJustPlayEngine,
}


async def search_profile(user_telegram_id: int, profile_type: int) -> Union[Profile, None]:
    engine_class = SEARCH_ENGINES[profile_type]
    engine = engine_class(user_telegram_id, profile_type)
    await engine.init()
    return await engine.search()
