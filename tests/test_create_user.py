import allure
import requests
import config
from helpers import User


@allure.story("User Registration Tests")
class TestCreateNewUserStellarBurger:

    @allure.title("Create a unique new user")
    @allure.description("Test the creation of a new unique user and validate the response.")
    def test_create_new_user_unique(self):
        payload = User.register_new_user()
        response = requests.post(config.CREATE_USER_PATH, json=payload)
        assert response.status_code == 200 and response.json()["success"] is True
        token = response.json()["accessToken"]
        requests.delete(config.DELETE_USER_PATH, headers={"Authorization": f"Bearer {token}"})

    @allure.title("Create user that already exists")
    @allure.description("Test the behavior when attempting to create a user that already exists.")
    def test_create_user_exists(self):
        payload = User.register_new_user()
        response_1 = requests.post(config.CREATE_USER_PATH, json=payload)
        token = response_1.json()["accessToken"]
        response_2 = requests.post(config.CREATE_USER_PATH, json=payload)
        assert response_2.status_code == 403 and response_2.json()["success"] is False
        requests.delete(config.DELETE_USER_PATH, headers={"Authorization": f"Bearer {token}"})

    @allure.title("Create user with empty fields")
    @allure.description("Test the creation of a user with missing required fields (password) and validate the error "
                        "response.")
    def test_create_user_empty_field(self):
        payload = {
            "email": "test@example.com",
            "name": "TestUser"
        }
        response = requests.post(config.CREATE_USER_PATH, json=payload)
        assert response.status_code == 403 and response.json()["success"] is False
        assert response.json()["message"] == "Email, password and name are required fields"
