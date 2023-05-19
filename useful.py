def isInt(str):
    try:
        float(str)
    except ValueError:
        return False
    return float(str).is_integer()