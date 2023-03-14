import redis
import json

r = redis.Redis(
    host='localhost',
    port=6379,
) 

def get_user(id: str):
    # return {key.decode(): value.decode() for key, value in r.hgetall(id).items()}
    dict_bytes = r.get(id)

    dict_str = dict_bytes.decode('utf-8')

    my_dict = json.loads(dict_str)

    return my_dict


def set_user(id: str, data: dict):
    r.set(id, bytes(json.dumps(data), "utf-8"))


def is_token_exist(id: str):
    data = get_user(id)
    if not data.get("token"):
        return False
    return data.get("token")

# if r.ping():
#     print("PONG")
# else:
#     print("Connection failed!")
# data = r.hgetall("345345345")

# print(data)

# normal_dict = {key.decode(): value.decode() for key, value in data.items()}

# print(normal_dict)

# print(normal_dict["id"])