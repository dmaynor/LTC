def parse_int(s):
    try:
        return (True, int(s))
    except ValueError as e:
        return (False, str(e))
