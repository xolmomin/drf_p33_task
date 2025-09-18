from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apps.views import ProductListAPIView, LoginAPIView, SendCodeAPIView
TokenObtainPairView
urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login', LoginAPIView.as_view(), name='register'),
    path('products', ProductListAPIView.as_view(), name='product-list'),
]
