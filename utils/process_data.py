from utils.forms import who_search_form
from loader import _


async def process_data(raw_data: dict):
    data = {}

    profile_type = raw_data.pop('profile_type')

    raw_data.pop('country')
    raw_data.pop('region')

    data['profile_type'] = profile_type
    data['photo'] = raw_data.pop('photo')
    data['games'] = raw_data.pop('games')
    data['age'] = raw_data.pop('age')
    data['gender'] = raw_data.pop('gender')
    data['name'] = raw_data.pop('name')
    data['city'] = raw_data.pop('city')

    if profile_type == who_search_form.person_in_real_life.id:
        data['description'] = _(
            'О себе: <b>{about_yourself}</b>\n'
            'Хобби: <b>{hobby}</b>'
        ).format(about_yourself=raw_data.pop('about_yourself'), hobby=raw_data.pop('hobby'))

        data['additional'] = raw_data
    elif profile_type == who_search_form.just_play.id:
        data['description'] = _(
            'Что-то о себе: <b>{about_yourself}</b>\n'
            'К/Д: <b>{call_down}</b>'
        ).format(about_yourself=raw_data.pop('about_yourself'), call_down=raw_data.pop('call_down'))

        data['additional'] = raw_data
    elif profile_type == who_search_form.team.id:
        pass

    return data
