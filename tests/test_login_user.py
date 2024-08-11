import allure
import requests
import config
from helpers import User


@allure.story("User Login Tests")
class TestLoginUser:

    @allure.title("Login with an existing user")
    @allure.description("Test the login functionality for an existing user.")
    def test_existing_user_login(self, create_user):
        payload = create_user[2]
        response = requests.post(config.LOGIN_USER_PATH, json=payload)
        assert response.status_code == 200 and response.json()["success"] is True

    @allure.title("Login with a non-existing user")
    @allure.description("Test the login functionality with incorrect credentials.")
    def test_non_existing_user_login(self):
        payload = User.register_new_user_without_name()
        response = requests.post(config.LOGIN_USER_PATH, json=payload)
        assert response.status_code == 401 and response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"
