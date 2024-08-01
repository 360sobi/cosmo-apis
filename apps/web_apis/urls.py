from django.urls import path, include
from .views import Dashboard, Product, Category, Order, complete_order_view

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard-api'),
    path('product/', Product.as_view(), name='product-api'),
    path('categories/', Category.as_view(), name='list-categories-api'),
    path('orders/', include([
        path('', Order.as_view(), name='list-orders-api'),
        path('complete', complete_order_view, name='complete-order-api'),
    ]))
]