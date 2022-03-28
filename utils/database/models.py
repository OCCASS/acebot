from typing import Union, Dict

import sqlalchemy.sql
from gino import Gino

db = Gino()


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)


class Region(db.Model):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    country_id = db.Column(None, db.ForeignKey('country.id'))


class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    region_id = db.Column(None, db.ForeignKey('region.id'))


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

    @classmethod
    async def as_dict(cls, user_telegram_id) -> Union[Dict, None]:
        user = await User.query.where(User.telegram_id == user_telegram_id).gino.first()
        if user:
            return {'telegram_id': user_telegram_id, 'name': user.name, 'username': user.username,
                    'locale': user.locale, 'gender': user.gender, 'age': user.age, 'games': user.games}

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
    city = db.Column(None, db.ForeignKey('city.id'))

    async def as_dict(self) -> Union[Dict, None]:
        user = await User.query.where(User.id == self.user_id).gino.first()
        profile = await Profile.query.where(Profile.user_id == user.id).gino.first()
        if profile:
            return {'user_id': user.id, 'photo': self.photo, 'type': self.type,
                    'description': self.description, 'additional': self.additional, 'city': self.city}
        return


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
