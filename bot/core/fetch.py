from bot.core.redis_db import is_token_exist, set_user
from bot.core.api import get



def fetch(message):
    _token = is_token_exist(str(message.from_id))
    _user = get("/api/v1/private/items/my", auth_token=_token)
    _user = {"token": _token, "saved": _user.json()}
    set_user(message.from_id, _user)