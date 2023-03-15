import json
import requests
from bot.core.config import settings


def post(url, body=None, auth_token=None):
    r = requests.post(f"{settings.SERVER_IP}{url}", json=body, headers={"Authorisation":auth_token})
    return r


def get(url, auth_token=None):
    r = requests.get(f"{settings.SERVER_IP}{url}", headers={"Authorisation":auth_token})
    return r


def verify_token(token):
    r = get(f"/api/v1/public/tools/verify", auth_token=token)
    if r.status_code != 200:
        return False
    return r
