from service.data_unifier._base import BaseDataUnifier
from service.forms import play_level_form
from loader import _


class PeopleIRLDataUnifier(BaseDataUnifier):
    async def fill_description(self):
        self._data['description'] = _(
            'О себе: <b>{about_yourself}</b>\n'
            'Хобби: <b>{hobby}</b>'
        ).format(
            about_yourself=self._raw_data.pop('about_yourself'),
            hobby=self._raw_data.pop('hobby')
        )


class JustPlayDataUnifier(BaseDataUnifier):
    async def fill_description(self):
        play_level = await play_level_form.get_by_id(self._raw_data.pop('play_level'))
        play_level = play_level.text
        self._data['description'] = _(
            'Что-то о себе: <b>{about_yourself}</b>\n'
            'К/Д: <b>{call_down}</b>\n'
            'Уровень игры: {play_level}'
        ).format(
            about_yourself=self._raw_data.pop('about_yourself'),
            call_down=self._raw_data.pop('call_down'),
            play_level=play_level
        )
