from django.urls import path

from apps.views import ProductListAPIView, LoginAPIView

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='register'),
    path('products', ProductListAPIView.as_view(), name='product-list'),
]
