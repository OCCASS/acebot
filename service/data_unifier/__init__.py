from data.types import ProfileTypes
from service.data_unifier.unifiers import PeopleIRLDataUnifier, JustPlayDataUnifier

DATA_UNIFIERS = {
    ProfileTypes.PERSON_IRL: PeopleIRLDataUnifier,
    ProfileTypes.JUST_PLAY: JustPlayDataUnifier
}


async def unify_data(raw_data: dict, user_telegram_id: int):
    profile_type = raw_data.get('profile_type')
    data_formatter_class = DATA_UNIFIERS[profile_type]
    data_unifier = data_formatter_class(raw_data, user_telegram_id)
    await data_unifier.init()
    await data_unifier.unify()
    return data_unifier.data
