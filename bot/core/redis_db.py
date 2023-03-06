import redis

r = redis.Redis(
    host='localhost',
    port=6379,
) 

def get_user(id: str):
    return {key.decode(): value.decode() for key, value in r.hgetall(id).items()}


def set_user(id: str, data: dict):
    return r.hset(id, data)


def is_token_exist(id: str):
    data = {key.decode(): value.decode() for key, value in r.hgetall(id).items()}
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