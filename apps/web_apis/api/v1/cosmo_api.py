import base64

import requests
from django.conf import settings
from html2text import html2text

from apps.web_apis.constants import *


class CosmoAPI:

    @staticmethod
    def _get_headers():
        # Base64 encode the credentials
        credentials = f"{settings.WC_CONSUMER_KEY}:{settings.WC_CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        # Set up and return the headers
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

    @staticmethod
    def _get_transformed_url(endpoint, base_url=WC_BASE_URL, **q_params):
        url = f'{base_url}{endpoint}'
        if q_params:
            url = f'{url}?'
            url += '&'.join([f'{q_param}={q_params[q_param][0]}' for q_param in q_params.keys()])

        return url

    def _make_request(self, endpoint, request_type, base_url=WC_BASE_URL, q_params=None, **kwargs):
        if q_params is None:
            q_params = {}
        url = self._get_transformed_url(endpoint, base_url, **q_params)
        method_map = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "PATCH": requests.patch,
            "DELETE": requests.delete,
        }
        response = method_map.get(request_type)(url, headers=self._get_headers(), **kwargs)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _transform_product(product):
        product['description'] = html2text(product['description'])
        product['short_description'] = html2text(product['short_description'])

    @staticmethod
    def _transform_store(store):
        store['vendor_description'] = html2text(store['vendor_description'])
        store['vendor_policies']['shipping_policy'] = html2text(store['vendor_policies']['shipping_policy'])
        store['vendor_policies']['refund_policy'] = html2text(store['vendor_policies']['refund_policy'])
        store['vendor_policies']['cancellation_policy'] = html2text(store['vendor_policies']['cancellation_policy'])

    def get_dashboard(self, **q_params):
        data = self._make_request('products', "GET", q_params)
        [self._transform_product(product) for product in data]
        return data

    def get_product(self, product_id):
        data = self._make_request(f'products/{product_id}', "GET")
        self._transform_product(data)
        return data

    def get_category(self, **q_params):
        return self._make_request('products/categories', "GET", q_params)

    def get_orders(self, **q_params):
        return self._make_request('orders', "GET", q_params)

    def create_order(self, data):
        return self._make_request('orders', "POST", json=data)

    def complete_order(self, order_id):
        complete_data = {"status": "completed"}
        return self._make_request(f'orders/{order_id}', "PUT", json=complete_data)

    def delete_order(self, order_id):
        return self._make_request(f'orders/{order_id}', "DELETE")

    def get_stores(self, **q_params):
        data = self._make_request('store-vendors', "GET", base_url=WCFMMP_BASE_URL, q_params=q_params)
        [self._transform_store(store) for store in data]
        return data

    def get_store(self, store_id):
        data = self._make_request(f'store-vendors/{store_id}', "GET", base_url=WCFMMP_BASE_URL)
        self._transform_store(data)
        return data

    def get_store_products(self, store_id):
        data = self._make_request(f'store-vendors/{store_id}/products', "GET", base_url=WCFMMP_BASE_URL)
        [self._transform_product(product) for product in data]
        return data
