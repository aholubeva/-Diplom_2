import requests
from helpers import register_new_user
import allure
from config import Config
from helpers import get_ingredients_list
from helpers import generate_invalid_ingredients_id


class TestCreateOrder:

    @allure.title('Проверяем создание заказа с ингредиентами и без авторизации, запрос возвращает код ответа 200 OK')
    def test_create_order_without_auth_code_200(self):
        ingredients_list = get_ingredients_list()

        payload = {
            "ingredients": ingredients_list
        }
        response = requests.post(f"{Config.url}/orders", data=payload)
        assert response.status_code == 200
        assert response.json()['success'] == True

    @allure.title('Проверяем создание заказа с ингредиентами и с авторизацией, запрос возвращает код ответа 200 OK и данные пользователя')
    def test_create_order_with_auth_code_200(self):
        email, password, name, response_status_code, response_status_text, access_token = register_new_user()
        ingredients_list = get_ingredients_list()

        payload = {
            "ingredients": ingredients_list
        }
        headers = {
            "Authorization": access_token
        }
        response = requests.post(f"{Config.url}/orders", data=payload, headers = headers)
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert f'"name":"{name}","email":"{email}"' in response.text

    @allure.title('Проверяем создание заказа без ингредиентов и без авторизации, запрос возвращает код ответа 400 Bad Request')
    def test_create_order_without_ingredients_code_400(self):
        ingredients_list = []

        payload = {
            "ingredients": ingredients_list
        }
        response = requests.post(f"{Config.url}/orders", data=payload)
        assert response.status_code == 400
        assert response.json()['message'] == "Ingredient ids must be provided"

    @allure.title('Проверяем создание заказа с неверным хэшем ингредиентов и без авторизации, запрос возвращает код ответа 500 Internal Server Error')
    def test_create_order_without_ingredients_code_500(self):
        ingredients_list = generate_invalid_ingredients_id()
        print(ingredients_list)

        payload = {
            "ingredients": ingredients_list
        }
        response = requests.post(f"{Config.url}/orders", data=payload)
        assert response.status_code == 500













