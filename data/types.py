class BaseTypes:
    types = []

    def __new__(cls, *args, **kwargs):
        __types = []
        for var, value in cls.__dict__.items():
            if not var.startswith('__'):
                __types.append(value)

        cls.types = __types
        return cls

    @classmethod
    def last(cls):
        return cls.types[-1]


class ProfileTypes(BaseTypes):
    PERSON_IRL = 1  # Person in real life
    JUST_PLAY = 2
    TEAM = 3


class WhoLookingForTypes(BaseTypes):
    GUYS = 1
    GIRLS = 2
    GUYS_AND_GIRLS = 3


class GenderTypes(BaseTypes):
    GUY = 1
    GIRL = 2


class ModificationTypes(BaseTypes):
    GENDER = 1  # All genders (guys and girls)
    GAMES = 2  # All games


class ComplainTypes(BaseTypes):
    MATERIAL_FOR_ADULTS = 1
    SALE_OF_GOODS = 2
    DOES_NOT_ANSWER = 3
    OTHER = 4


class BanDurationTypes(BaseTypes):
    ONE_DAY = 1
    ONE_MONTH = 2
    FOREVER = 3
