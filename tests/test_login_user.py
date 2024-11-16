import requests
from helpers import register_new_user
import allure
from config import Config
from helpers import generate_new_email_password_name


class TestLoginUser:

    @allure.title('Проверяем успешный логин существующего пользователя, запрос возвращает код ответа 200 OK')
    def test_success_login_user_code_200(self):
        email, password, name, response_status_code, response_status_text, access_token = register_new_user()
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{Config.url}/auth/login", data=payload)
        assert response.status_code == 200 and f'"email":"{email}","name":"{name}"' in response.text


    @allure.title('Проверяем, что юзер не может залогиниться с невалидным логином или паролем, запрос возвращает ошибку с кодом 401')
    def test_courier_login_with_not_existing_user_error_401(self):
        new_email, new_password, new_name = generate_new_email_password_name()
        payload = {
            "email": new_email,
            "password": new_password
        }

        response = requests.post(f"{Config.url}/auth/login", data=payload)
        assert (response.status_code == 401)
        assert response.json()['success'] == False
        assert response.json()['message'] ==  "email or password are incorrect"

