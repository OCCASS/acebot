from typing import Union, Dict

import sqlalchemy.sql
from gino import Gino

db = Gino()


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    names = db.Column(db.JSON, nullable=False)


class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    names = db.Column(db.JSON, nullable=False)
    country_id = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200))
    locale = db.Column(db.String(2))
    gender = db.Column(None, db.ForeignKey('gender.id'))
    age = db.Column(db.Integer)
    games = db.Column(db.JSON)
    cities = db.Column(db.JSON)

    async def get_countries(self):
        countries = []
        for city in self.cites:
            city = await City.query.where(City.id == city).gino.first()
            country = await Country.query.where(Country.id == city.country_id).gino.first()
            countries.append(country)

        return countries

    @classmethod
    async def as_dict(cls, user_telegram_id) -> Union[Dict, None]:
        user = await User.query.where(User.telegram_id == user_telegram_id).gino.first()
        if user:
            return {'telegram_id': user_telegram_id, 'name': user.name, 'username': user.username,
                    'locale': user.locale, 'gender': user.gender, 'age': user.age, 'games': user.games,
                    'cities': user.cities}

        return


class Profile(db.Model):
    __tablename__ = 'profile'
    query: sqlalchemy.sql.Select

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(None, db.ForeignKey('user.id'))
    photo = db.Column(db.String(200))
    type = db.Column(db.Integer)
    description = db.Column(db.String(400))
    additional = db.Column(db.JSON)
    modification_type = db.Column(db.Integer)
    last_seen_profile_id = db.Column(None, db.ForeignKey('profile.id'), default=None)
    enable = db.Column(db.Boolean, default=True)
    modified_at = db.Column(db.DateTime)

    async def as_dict(self) -> Union[Dict, None]:
        return {'user_id': self.user_id, 'photo': self.photo, 'profile_type': self.type,
                'description': self.description, 'additional': self.additional}


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))


class SeenProfiles(db.Model):
    __tablename__ = 'seen_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    who_saw_profile_id = db.Column(None, db.ForeignKey('profile.id'))
    who_seen_profile_id = db.Column(None, db.ForeignKey('profile.id'))
    seen_at = db.Column(db.DateTime)


class Complain(db.Model):
    __tablename__ = 'complain'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    to_profile_id = db.Column(None, db.ForeignKey('profile.id'))
    from_profile_id = db.Column(None, db.ForeignKey('profile.id'))
    complain_type = db.Column(db.Integer)
    sent_at = db.Column(db.DateTime)


class Ban(db.Model):
    __tablename__ = 'ban'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    to_user_id = db.Column(None, db.ForeignKey('user.id'))
    from_date = db.Column(db.DateTime)
    type = db.Column(db.Integer)


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    liked_profile_id = db.Column(None, db.ForeignKey('profile.id'))
    who_liked_profile_id = db.Column(None, db.ForeignKey('profile.id'))
    message = db.Column(db.String(), default=None)
    is_like_seen = db.Column(db.Boolean, default=False)
