import re

async def represents_int(value, return_value=False):
    regex = r"^[0-9]*$"
    
    if not re.fullmatch(regex, value):
        return False

    if return_value:
        return int(value)
    
    return True