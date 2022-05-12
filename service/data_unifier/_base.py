from loader import db


class BaseDataUnifier:
    def __init__(self, raw_data: dict, user_telegram_id: int):
        self._raw_data = raw_data
        self._user_telegram_id = user_telegram_id

        self._user = None
        self._data = dict()

    async def init(self):
        await self._get_user()

    async def unify(self):
        self._remove_unnecessary_keys()
        self._fill_general_keys()
        await self.fill_description()
        self._fill_additional()

    @property
    def data(self):
        return self._data

    async def _get_user(self):
        self._user = await db.get_user_by_telegram_id(self._user_telegram_id)

    def _remove_unnecessary_keys(self):
        unnecessary_keys = ['country']
        for key in unnecessary_keys:
            self._raw_data.pop(key, None)

    def _fill_general_keys(self):
        self._data['profile_type'] = self._raw_data.pop('profile_type')
        self._data['photo'] = self._raw_data.pop('photo')
        self._data['games'] = self._raw_data.pop('games', None) or self._user.games
        self._data['age'] = self._raw_data.pop('age', None) or self._user.age
        self._data['gender'] = self._raw_data.pop('gender', None) or self._user.gender
        self._data['name'] = self._raw_data.pop('name', None) or self._user.name
        self._data['city'] = self._raw_data.pop('city', None) or self._user.city

    async def fill_description(self):
        raise NotImplementedError

    def _fill_additional(self):
        self._data['additional'] = self._raw_data
