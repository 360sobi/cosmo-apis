from django.urls import path, include

from .api.v1.viewsets import Dashboard, Product, Category, Order, complete_order_view, delete_order_view, Store, Stores, \
    StoreProducts

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard-api'),
    path('product/', Product.as_view(), name='product-detail-api'),
    path('categories/', Category.as_view(), name='list-categories-api'),
    path('stores/', Stores.as_view(), name='list-stores-api'),
    path('store/', Store.as_view(), name='store-detail-api'),
    path('store-products/', StoreProducts.as_view(), name='store-products-api'),
    path('orders/', include([
        path('', Order.as_view(), name='list-orders-api'),
        path('complete', complete_order_view, name='complete-order-api'),
        path('delete', delete_order_view, name='delete-order-api'),
    ]))
]
