import redis
import json

r = redis.Redis(
    host='localhost',
    port=6379,
) 

def get_user(id: str):
    dict_bytes = r.get(id)

    if not dict_bytes:
        return {}

    dict_str = dict_bytes.decode('utf-8')

    my_dict = json.loads(dict_str)

    return my_dict


def set_user(id: str, data: dict):
    r.set(id, bytes(json.dumps(data), "utf-8"))


def logout(id: str):
    r.delete(id)


def is_token_exist(id: str):
    data = get_user(id)
    if not data.get("token"):
        return False
    return data.get("token")