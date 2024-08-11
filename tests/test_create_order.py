import allure
import requests
import config


@allure.suite("Order Creation Tests")
class TestCreateOrder:

    @allure.title("Create order with authorization")
    @allure.description("This test verifies that an authorized user can successfully create an order with valid "
                        "ingredients.")
    def test_create_order_with_authorization(self, login_user):
        bearer_token = login_user

        ingredients_response = requests.get(config.INGREDIENTS_PATH)
        assert ingredients_response.status_code == 200, "Failed to get ingredients"

        ingredients_data = ingredients_response.json()
        assert "data" in ingredients_data, "No ingredients data found in the response"

        ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]

        payload = {
            "ingredients": ingredient_ids
        }
        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Create order without authorization")
    @allure.description("This test verifies that an order can be created without user authorization.")
    def test_create_order_without_authorization(self):
        ingredients_response = requests.get(config.INGREDIENTS_PATH)
        assert ingredients_response.status_code == 200

        ingredients_data = ingredients_response.json()
        ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]

        payload = {
            "ingredients": ingredient_ids
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Create order with ingredients")
    @allure.description("This test verifies that an order can be created with valid ingredients.")
    def test_create_order_with_ingredients(self, login_user):
        bearer_token = login_user

        ingredients_response = requests.get(config.INGREDIENTS_PATH)
        assert ingredients_response.status_code == 200

        ingredients_data = ingredients_response.json()
        ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]

        payload = {
            "ingredients": ingredient_ids
        }
        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Create order without ingredients")
    @allure.description("This test verifies that an order creation attempt without ingredients returns the correct "
                        "error.")
    def test_create_order_without_ingredients(self, login_user):
        bearer_token = login_user

        payload = {
            "ingredients": []
        }
        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Create order with invalid ingredient hash")
    @allure.description("This test verifies that an order creation attempt with an invalid ingredient hash returns a "
                        "500 Internal Server Error.")
    def test_create_order_with_invalid_ingredient_hash(self, login_user):
        bearer_token = login_user

        payload = {
            "ingredients": ["######"]
        }
        headers = {'Authorization': bearer_token, 'Content-type': 'application/json'}
        response = requests.post(config.CREATE_ORDER_PATH, json=payload, headers=headers)

        assert response.status_code == 500
        assert "Internal Server Error" in response.text
