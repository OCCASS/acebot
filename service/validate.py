from data.config import BAD_WORDS
from data.types import ProfileTypes
from urlextract import URLExtract


def is_int(value: str):
    try:
        int(value)
    except (ValueError, TypeError):
        return False
    else:
        return True


def is_float(value: str):
    try:
        float(value)
    except (ValueError, TypeError):
        return False
    else:
        return True


async def is_correct_profile_type(profile_type: int):
    if profile_type > ProfileTypes.last() or profile_type < 1:
        return False
    return True


def validate_age(age: int):
    return 10 <= age <= 99


def validate_name(name: str):
    return len(name) <= 30


def is_url_in_text(text: str):
    extract = URLExtract()
    return bool(extract.find_urls(text))


def is_bad_word_in_text(text: str):
    text = text.lower()
    for word in BAD_WORDS:
        if word in text:
            return True

    return False
