from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProductModelViewSet, LoginAPIView, SendCodeAPIView, CategoryListAPIView, \
    CartItemListCreateAPIView, OrderListAPIView, CartConfirmAPIView, CustomTokenRefreshView

router = DefaultRouter(trailing_slash=False)
router.register('products', ProductModelViewSet)

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token', CustomTokenRefreshView.as_view(), name='token_refresh'),
    # path('login', LoginAPIView.as_view(), name='register'),
    # path('products', ProductListAPIView.as_view(), name='product-list'),
    path('', include(router.urls)),
    path('categories', CategoryListAPIView.as_view(), name='category-list'),
    path('cart-items', CartItemListCreateAPIView.as_view(), name='cart-item-list'),
    path('cart/confirm', CartConfirmAPIView.as_view(), name='cart-confirm'),
    path('orders', OrderListAPIView.as_view(), name='order-create'),
]
