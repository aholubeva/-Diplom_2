import requests
from helpers import register_new_user
import allure
from config import Config
from helpers import generate_new_email_password_name


class TestUpdateUser:

    @allure.title('Проверяем изменение данных пользователя без авторизации, запрос возвращает код ответа 401 Unauthorized')
    def test_update_user_without_auth_code_401(self):
        register_new_user()
        new_email, new_password, new_name = generate_new_email_password_name()
        payload = {
            "email": new_email,
            "password": new_password,
            "name": new_name
        }
        response = requests.patch(f"{Config.url}/auth/user", data=payload)
        assert response.status_code == 401
        assert response.json()['success'] == False
        assert response.json()['message'] == "You should be authorised"

    @allure.title('Проверяем успешное изменение данных пользователя с авторизацией, запрос возвращает код ответа 200 OK')
    def test_update_user_with_auth_code_200(self):
        email, password, name, response_status_code, response_status_text, access_token = register_new_user()
        new_email, new_password, new_name = generate_new_email_password_name()
        payload = {
            "email": new_email,
            "password": new_password,
            "name": new_name
        }
        headers = {
            "Authorization": access_token
        }
        response = requests.patch(f"{Config.url}/auth/user", data=payload, headers = headers)
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert f'"email":"{new_email}","name":"{new_name}"' in response.text

