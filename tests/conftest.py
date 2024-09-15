import sys
import os
import pytest
import requests
from ..helpers import User
from .. import config


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def create_user():
    payload = User.register_new_user()

    response = requests.delete(config.DELETE_USER_PATH, json=payload)

    if response.status_code not in [200, 404]:
        raise RuntimeError(f"Failed to delete existing user. Status code: {response.status_code}")

    response = requests.post(config.CREATE_USER_PATH, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"User creation failed. Status code: {response.status_code}")

    token = response.json().get("accessToken")
    if not token:
        raise RuntimeError(f"No accessToken found in response. Response body: {response.json()}")

    bearer_token = f"Bearer {token}"
    yield response.json()["user"], bearer_token, payload

    response = requests.delete(config.DELETE_USER_PATH, headers={"Authorization": bearer_token})
    if response.status_code not in [200, 404]:  # Suppress the warning for 404
        raise RuntimeError(f"Failed to delete user during cleanup. Status code: {response.status_code}")


@pytest.fixture
def login_user(create_user):
    user_data = create_user[2]
    response = requests.post(config.LOGIN_USER_PATH, json=user_data)

    if response.status_code != 200:
        raise RuntimeError(f"Login failed. Status code: {response.status_code}")

    token = response.json().get("accessToken")
    if not token:
        raise RuntimeError(f"No accessToken found in login response. Response body: {response.json()}")

    bearer_token = f"Bearer {token}"

    if bearer_token.count("Bearer ") > 1:
        bearer_token = bearer_token.replace("Bearer ", "", 1)

    return bearer_token


