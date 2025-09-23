from django.urls import path

from apps.views import ProductListAPIView, LoginAPIView, SendCodeAPIView, CategoryListAPIView, \
    CartItemListCreateAPIView, OrderListAPIView, CartConfirmAPIView, CustomTokenRefreshView

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token', CustomTokenRefreshView.as_view(), name='token_refresh'),
    # path('login', LoginAPIView.as_view(), name='register'),
    path('products', ProductListAPIView.as_view(), name='product-list'),
    path('categories', CategoryListAPIView.as_view(), name='category-list'),
    path('cart-items', CartItemListCreateAPIView.as_view(), name='cart-item-list'),
    path('cart/confirm', CartConfirmAPIView.as_view(), name='cart-confirm'),
    path('orders', OrderListAPIView.as_view(), name='order-create'),
]
