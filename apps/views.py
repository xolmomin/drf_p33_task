from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import Product
from apps.serializers import ProductListModelSerializer, CustomAccessTokenSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomAccessTokenSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
