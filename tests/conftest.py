import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config


import pytest
import requests
from helpers import User


@pytest.fixture
def create_user():
    payload = User.register_new_user()

    requests.delete(config.DELETE_USER_PATH, json=payload)

    response = requests.post(config.CREATE_USER_PATH, json=payload)

    if response.status_code != 200:
        print(f"User creation failed with status code {response.status_code}")
        print(f"Response body: {response.json()}")
        assert False, "User creation failed"

    token = response.json().get("accessToken")
    if not token:
        print(f"Response body: {response.json()}")
        assert False, "No accessToken found in response"

    bearer_token = f"Bearer {token}"
    yield response.json()["user"], bearer_token, payload

    # Cleanup after the test
    requests.delete(config.DELETE_USER_PATH, headers={"Authorization": bearer_token})


@pytest.fixture
def login_user(create_user):
    user_data = create_user[2]
    response = requests.post(config.LOGIN_USER_PATH, json=user_data)
    assert response.status_code == 200
    token = response.json().get("accessToken")
    bearer_token = f"Bearer {token}"

    if bearer_token.count("Bearer ") > 1:
        bearer_token = bearer_token.replace("Bearer ", "", 1)

    return bearer_token
