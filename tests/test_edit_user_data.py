import allure
import requests
from .. import config
from ..helpers import User
from tests.utils import clean_token, patch_user_data


@allure.suite("User Data Edit Tests")
class TestUserEditData:

    @allure.title("Edit authorized user's name")
    @allure.description("Test the functionality of editing an authorized user's name.")
    def test_edit_authorized_user_name(self, create_user):
        _, token, _ = create_user
        token = clean_token(token)
        new_name = User.update_user_data()["name"]
        response = patch_user_data(token, {"name": new_name})
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["name"] == new_name

    @allure.title("Edit authorized user's email")
    @allure.description("Test the functionality of editing an authorized user's email.")
    def test_edit_authorized_user_email(self, create_user):
        _, token, _ = create_user
        token = clean_token(token)
        new_email = User.update_user_data()["email"]
        response = patch_user_data(token, {"email": new_email})
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == new_email

    @allure.title("Attempt to edit user data without authorization")
    @allure.description("Test the response when trying to edit user data without authorization.")
    def test_edit_unauthorized_user_data(self):
        new_data = User.update_user_data()
        response = requests.patch(config.UPDATE_USER_PATH, json=new_data)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"
