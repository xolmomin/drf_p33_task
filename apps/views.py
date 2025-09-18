from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Product
from apps.serializers import ProductListModelSerializer


class LoginAPIView(APIView):

    def post(self, request):
        return Response({}, status.HTTP_200_OK)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
