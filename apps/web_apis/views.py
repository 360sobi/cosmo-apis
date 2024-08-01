import requests
import stripe
from django.conf import settings
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.web_apis.utils import get_dashboard, get_product, get_category, get_orders, create_order, complete_order

stripe.api_key = settings.STRIPE_API_KEY


class Dashboard(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = get_dashboard(**request.GET)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Product(APIView):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')

        try:
            data = get_product(product_id)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Category(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = get_category(**request.GET)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Order(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = get_orders(**request.GET)
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
                        "value": payment_intent.id
                    }
                ]
            }
            order_payload = {**request.data, **additional_payload}
            data = create_order(order_payload)
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(["PUT"])
def complete_order_view(request):
    order_id = request.GET.get('order_id')
    try:
        data = complete_order(order_id)
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

