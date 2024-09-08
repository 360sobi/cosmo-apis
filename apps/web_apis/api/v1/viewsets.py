import requests
import stripe
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.web_apis.api.v1.cosmo_api import CosmoAPI

stripe.api_key = settings.STRIPE_API_KEY

cosmo_api = CosmoAPI()


class Dashboard(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = cosmo_api.get_dashboard(**request.GET)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Product(APIView):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')

        try:
            data = cosmo_api.get_product(product_id)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Category(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = cosmo_api.get_category(**request.GET)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Order(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = cosmo_api.get_orders(**request.GET)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:

            # Create a payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=request.data.pop("amount"),  # Amount in cents
                currency="usd",
                payment_method_types=["card"]
            )

            additional_payload = {
                "payment_method": "stripe",
                "payment_method_title": "Stripe",
                "set_paid": False,
                "meta_data": [
                    {
                        "key": "_stripe_payment_intent_id",
                        "value": payment_intent.client_secret
                    }
                ]
            }
            order_payload = {**request.data, **additional_payload}
            data = cosmo_api.create_order(order_payload)
            response_data = {"order_id": data["id"], "payment_intent_id": data["meta_data"][0]["value"],
                             "order_status": data["status"]}
            return Response(response_data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def complete_order_view(request):
    order_id = request.GET.get('order_id')
    try:
        data = cosmo_api.complete_order(order_id)
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_order_view(request):
    order_id = request.GET.get('order_id')
    try:
        data = cosmo_api.delete_order(order_id)
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
