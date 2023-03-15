from functools import wraps
from bot.core.fetch import fetch
from bot.core.redis_db import is_token_exist
from bot.core.api import verify_token

    
def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        _token = is_token_exist(str(args[0].from_user.id))
        if _token and verify_token(_token):
            return await func(*args, **kwargs)
        return await args[0].answer("Unfortunaly you can't use commands, as you are not unauthorised, please use command /start and follow instructions.")
    return wrapper


def auto_fetch(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        _token = is_token_exist(str(args[0].from_user.id))
        fetch(args[0])
        return await func(*args, **kwargs)
    
    return wrapper