import requests
from django.conf import settings

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_SERVICE_KEY

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


# Функция для получения списка товаров
def get_supabase_products():
    url = f"{SUPABASE_URL}/rest/v1/products"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        return []


# Функция для добавления товара в корзину
def add_to_cart(user_id, product_id, quantity):
    url = f"{SUPABASE_URL}/rest/v1/cart"
    data = {"user_id": user_id, "product_id": product_id, "quantity": quantity}
    response = requests.post(url, json=data, headers=HEADERS)
    return response.status_code == 201
