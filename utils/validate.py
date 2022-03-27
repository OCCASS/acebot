async def is_int(value: str):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return False
    else:
        return True


async def is_float(value: str):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return False
    else:
        return True
