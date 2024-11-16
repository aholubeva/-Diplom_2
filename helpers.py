import faker
import requests
from config import Config
import secrets


def register_new_user():
    fake = faker.Faker()
    email = fake.email()
    password = fake.password()
    name = fake.name()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(f"{Config.url}/auth/register", data=payload)
    response_status_code = response.status_code
    response_status_text = response.text
    access_token = response.json()['accessToken']


    if response.status_code == 200:
        return email, password, name, response_status_code, response_status_text, access_token

def generate_new_email_password_name():
    fake = faker.Faker()
    new_email = fake.email()
    new_password = fake.password()
    new_name = fake.name()

    return new_email, new_password, new_name

def get_ingredients_list():   # в этой функции я сначала собираю все id ингредиентов в одном списке, а потом из этого списка забираю лишь 3 ингредиента, чтобы добавить в запрос при создании заказа
    response = requests.get(f"{Config.url}/ingredients")
    ingredients = response.json()['data']
    id_list = []
    ingredients_list = []

    for ingredient in ingredients:
        ingredient_id = ingredient['_id']
        id_list.append(ingredient_id)

    ingredients_list.append(id_list[0])
    ingredients_list.append(id_list[1])
    ingredients_list.append(id_list[2])

    return ingredients_list

def generate_invalid_ingredients_id():
    ingredients_list = []
    id_1 = secrets.token_hex(nbytes=11)
    id_2 = secrets.token_hex(nbytes=11)
    ingredients_list.append(id_1)
    ingredients_list.append(id_2)

    return ingredients_list

def create_orders_for_specific_user():
    email, password, name, response_status_code, response_status_text, access_token = register_new_user()
    ingredients_list = get_ingredients_list()
    payload = {
        "ingredients": ingredients_list
    }
    headers = {
        "Authorization": access_token
    }
    response = requests.post(f"{Config.url}/orders", data=payload, headers=headers)
    order_id = response.json()['order']['_id']

    return access_token, order_id







