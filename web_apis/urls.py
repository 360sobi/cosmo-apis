from django.urls import path
from .views import Dashboard, Product, Category

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard-api'),
    path('product/', Product.as_view(), name='product-api'),
    path('categories/', Category.as_view(), name='list-categories-api'),
]
