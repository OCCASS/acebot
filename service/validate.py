from data.types import ProfileTypes


async def is_int(value: str):
    try:
        int(value)
    except (ValueError, TypeError):
        return False
    else:
        return True


async def is_float(value: str):
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
