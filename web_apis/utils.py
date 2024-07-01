import html2text
import requests

from web_apis.constants import BASE_URL


def transform_product(product):
    product['title'] = product['title']['rendered']
    product['content'] = html2text.html2text(product['content']['rendered'])
    product['excerpt'] = html2text.html2text(product['excerpt']['rendered'])

    url = f"{BASE_URL}media/{product['featured_media']}"
    response = make_request(url)
    product['image_url'] = response['guid']['rendered']


def make_request(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data


def get_dashboard():
    products_url = f'{BASE_URL}product'
    data = make_request(products_url)
    for product in data:
        transform_product(product)
    return data


def get_product(product_id):
    product_url = f'{BASE_URL}product/{product_id}'
    data = make_request(product_url)
    transform_product(data)
    return data
