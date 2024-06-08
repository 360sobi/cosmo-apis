from django.urls import path
from .views import Dashboard, Product

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard-api'),
    path('product/', Product.as_view(), name='product-api'),
]
