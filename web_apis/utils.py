import requests

from web_apis.constants import BASE_URL


def make_request(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data


def get_dashboard():
    products_url = f'{BASE_URL}product'
    return make_request(products_url)


def get_products(product_id):
    product_url = f'{BASE_URL}product/{product_id}'
    return make_request(product_url)
