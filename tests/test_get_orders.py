import requests
import allure
from config import Config
from helpers import create_orders_for_specific_user


class TestGetOrders:

    @allure.title('Проверяем получение заказов пользователя без авторизации, запрос возвращает код ответа 401 Unauthorized.')
    def test_get_orders_without_auth_code_401(self):

        response = requests.get(f"{Config.url}/orders")
        assert response.status_code == 401
        assert response.json()['success'] == False
        assert response.json()['message'] == "You should be authorised"

    @allure.title('Проверяем получение заказов пользователя с авторизацией, запрос возвращает код ответа 200 OK.')
    def test_get_orders_wit_auth_code_200(self):
        access_token, order_id = create_orders_for_specific_user()
        headers = {
            "Authorization": access_token
        }
        response = requests.get(f"{Config.url}/orders", headers = headers)

        assert order_id in response.text
        assert response.json()['success'] == True
