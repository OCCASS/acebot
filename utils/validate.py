async def is_int(value: str):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return False
    else:
        return True
