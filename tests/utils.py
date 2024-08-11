import requests
import config


def patch_user_data(token, data):
    headers = {"Authorization": token}
    return requests.patch(config.UPDATE_USER_PATH, json=data, headers=headers)


def clean_token(token):
    if token.startswith("Bearer Bearer "):
        return token[len("Bearer "):]
    if token.startswith("Bearer "):
        return token[len("Bearer "):]
    return token
