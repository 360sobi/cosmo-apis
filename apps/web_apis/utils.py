import base64

import html2text
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

from apps.web_apis.constants import BASE_URL


def transform_product(product):
    product['description'] = html2text.html2text(product['description'])
    product['short_description'] = html2text.html2text(product['short_description'])


def make_request(url):
    response = requests.get(url, auth=HTTPBasicAuth(settings.WC_CONSUMER_KEY, settings.WC_CONSUMER_SECRET))
    response.raise_for_status()
    return response.json()


def get_headers():
    # Base64 encode the credentials
    credentials = f"{settings.WC_CONSUMER_KEY}:{settings.WC_CONSUMER_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # Set up and return the headers
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }


def get_transformed_url(url, **q_params):
    if q_params:
        url = f'{url}?'
        url += '&'.join([f'{q_param}={q_params[q_param][0]}' for q_param in q_params.keys()])

    return url


def get_dashboard(**q_params):
    url = get_transformed_url(f'{BASE_URL}products', **q_params)
    data = make_request(url)
    [transform_product(product) for product in data]
    return data


def get_product(product_id):
    url = f'{BASE_URL}products/{product_id}'
    data = make_request(url)
    transform_product(data)
    return data


def get_category(**q_params):
    url = get_transformed_url(f'{BASE_URL}products/categories', **q_params)
    return make_request(url)


def get_orders(**q_params):
    url = get_transformed_url(f'{BASE_URL}orders', **q_params)
    return make_request(url)


def create_order(data):
    url = get_transformed_url(f'{BASE_URL}orders')
    response = requests.post(url, json=data, headers=get_headers())
    response.raise_for_status()
    return response.json()


def complete_order(order_id):
    url = f'{BASE_URL}orders/{order_id}'
    complete_data = {"status": "completed"}
    response = requests.put(url, json=complete_data, headers=get_headers())
    response.raise_for_status()
    return response.json()
