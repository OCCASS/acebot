from service.data_unifier._base import BaseDataUnifier
from service.forms import play_level_form


class PeopleIRLDataUnifier(BaseDataUnifier):
    async def fill_description(self):
        self._data['description'] = '<b>О себе</b>: {about_yourself}\n\n<b>Хобби</b>: {hobby}'.format(
            about_yourself=self._raw_data.pop('about_yourself'), hobby=self._raw_data.pop('hobby'))


class JustPlayDataUnifier(BaseDataUnifier):
    async def fill_description(self):
        play_level = await play_level_form.get_by_id(self._raw_data.pop('play_level'))
        play_level = play_level.text
        self._data[
            'description'] = '<b>Что-то о себе</b>: {about_yourself}\n' \
                             '<b>К/Д</b>: {call_down}\n' \
                             '<b>Уровень игры</b>: {play_level}'.format(
            about_yourself=self._raw_data.pop('about_yourself'),
            call_down=self._raw_data.pop('call_down'),
            play_level=play_level)
