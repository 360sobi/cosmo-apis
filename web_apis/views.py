import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from web_apis.utils import get_dashboard, get_products


def make_response():
    pass


class Dashboard(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = get_dashboard()
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Product(APIView):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')

        try:
            data = get_products(product_id)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
