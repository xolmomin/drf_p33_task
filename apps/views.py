from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Product
from apps.serializers import ProductListModelSerializer, RegisterModelSerializer


class RegisterAPIView(APIView):
    serializer_class = RegisterModelSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer


"""
first_name
username
email
password
confirm_password

"""
