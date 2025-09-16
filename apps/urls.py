from django.urls import path

from apps.views import ProductListAPIView, RegisterAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('products', ProductListAPIView.as_view(), name='product-list'),
]
