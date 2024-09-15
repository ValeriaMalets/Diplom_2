import allure
import requests
from .. import config


@allure.suite("Order Creation Tests")
class TestCreateOrder:

    @allure.title("Create order with authorization")
    @allure.description("This test verifies that an authorized user can successfully create an order with valid "
                        "ingredients.")
    def test_create_order_with_authorization(self, login_user):
        bearer_token = login_user

        ingredients_response = requests.get(config.INGREDIENTS_PATH)
        ingredients_data = ingredients_response.json()
        ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data.get("data", [])[:2]]
        payload = {"ingredients": ingredient_ids}
        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)

    @allure.title("Create order without authorization")
    @allure.description("This test verifies that an order can be created without user authorization.")
    def test_create_order_without_authorization(self):
        ingredients_response = requests.get(config.INGREDIENTS_PATH)
        ingredients_data = ingredients_response.json()
        ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data.get("data", [])[:2]]
        payload = {"ingredients": ingredient_ids}
        headers = {'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)
        assert response.ok, "Order creation failed"

    @allure.title("Create order with ingredients")
    @allure.description("This test verifies that an order can be created with valid ingredients.")
    def test_create_order_with_ingredients(self, login_user):
        bearer_token = login_user
        ingredients_response = requests.get(config.INGREDIENTS_PATH)
        ingredients_data = ingredients_response.json()
        ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data.get("data", [])[:2]]
        payload = {"ingredients": ingredient_ids}
        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)
        assert response.ok, "Order creation failed"

    @allure.title("Create order without ingredients")
    @allure.description("This test verifies that an order creation attempt without ingredients returns the correct "
                        "error.")
    def test_create_order_without_ingredients(self, login_user):
        bearer_token = login_user
        payload = {"ingredients": []}
        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)
        assert response.status_code == 400, "Possible to create empty order"

    @allure.title("Create order with invalid ingredient hash")
    @allure.description("This test verifies that an order creation attempt with an invalid ingredient hash returns a "
                        "500 Internal Server Error.")
    def test_create_order_with_invalid_ingredient_hash(self, login_user):
        bearer_token = login_user
        payload = {"ingredients": ["######"]}
        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)
        assert response.status_code == 500, "Step 2: Expected status code 500 for invalid ingredient hash"
