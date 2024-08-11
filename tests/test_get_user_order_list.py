import allure
import requests
import config


@allure.suite("User Orders Tests")
class TestGetUserOrders:

    @allure.title("Get orders for authorized user")
    @allure.description("This test verifies that an authorized user can successfully retrieve their orders.")
    def test_get_orders_authorized_user(self, login_user):
        bearer_token = login_user

        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.get(config.GET_ORDERS_PATH, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.title("Get orders for unauthorized user")
    @allure.description("This test verifies that an unauthorized user cannot retrieve orders and receives a 401 "
                        "Unauthorized status.")
    def test_get_orders_unauthorized_user(self):
        response = requests.get(config.GET_ORDERS_PATH)

        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "You should be authorised"
