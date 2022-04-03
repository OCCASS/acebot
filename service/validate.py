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
