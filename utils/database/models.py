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
    city = db.Column(None, db.ForeignKey('city.id'))
    age = db.Column(db.Integer)
    games = db.Column(db.JSON)

    @property
    def region(self) -> int:
        return 0

    @property
    def country(self) -> int:
        return 0


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(None, db.ForeignKey('user.id'))
    photo = db.Column(db.String(200))
    type = db.Column(db.Integer)
    description = db.Column(db.String(400))
    additional = db.Column(db.JSON)


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
