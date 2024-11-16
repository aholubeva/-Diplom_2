import requests
from helpers import register_new_user
import pytest
import allure
from config import Config


class TestCreateUser:

    @allure.title('Проверяем успешное создание пользователя, запрос возвращает код ответа 200 OK')
    def test_success_create_user_code_200(self):
        email, password, name, response_status_code, response_status_text, access_token = register_new_user()
        assert response_status_code == 200 and f'"email":"{email}","name":"{name}"' in response_status_text

    @allure.title('Проверяем, что нельзя создать пользователя, который уже зарегистрирован, запрос возвращает ошибку с кодом 403 Forbidden')
    def test_create_existing_user_code_403(self):
        email, password, name, response_status_code, response_status_text, access_token = register_new_user()
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        second_response = requests.post(f"{Config.url}/auth/register", data=payload)
        assert (second_response.status_code == 403 and second_response.json()['success'] == False and second_response.json()['message'] == "User already exists")

    @pytest.mark.parametrize(
        "payload_data",
        [
            {"name": "", "email": "email", "password": "password"},
            {"name": "name", "email": "", "password": "password"},
            {"name": "name", "email": "email", "password": ""}

        ]
    )
    @allure.title('Проверяем, что нельзя создать юзера с пустым именем/или емейлом/или паролем, запрос возвращает ошибку с кодом 403 Forbidden')
    def test_create_user_with_empty_required_field_403(self, payload_data):

        payload = payload_data
        response = requests.post(f"{Config.url}/auth/register", data=payload)
        assert (response.status_code == 403 and response.json()['success'] == False and response.json()['message'] == "Email, password and name are required fields")

