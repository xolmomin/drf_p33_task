from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.models import Product, Category, CartItem, Order, OrderItem
from apps.serializers import ProductListModelSerializer, SendSmsCodeSerializer, \
    VerifySmsCodeSerializer, CategoryListModelSerializer, CartItemModelSerializer, OrderModelSerializer
from apps.utils import random_code, send_sms_code, check_sms_code


@extend_schema(tags=['Auth'])
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        phone = serializer.data['phone']
        send_sms_code(phone, code)
        return Response({"message": "send sms code"})


@extend_schema(tags=['Auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = check_sms_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    authentication_classes = ()


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListModelSerializer
    authentication_classes = ()


class CartItemListCreateAPIView(ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(cart__user=self.request.user)


class CartConfirmAPIView(APIView):
    permission_classes = IsAuthenticated,

    def post(self, request, *args, **kwargs):
        user = request.user

        order = Order.objects.create(user=user, total_amount=0)

        order_item_list = []
        total_amount = 0
        for cart_item in user.cart.cart_items.all():
            _quantity = cart_item.quantity
            _price = cart_item.product.price
            total_amount += _quantity * _price
            order_item_list.append(OrderItem(
                product=cart_item.product,
                quantity=_quantity,
                price=_price,
                order=order
            ))
        OrderItem.objects.bulk_create(order_item_list)
        order.total_amount = total_amount
        order.save()
        return Response({"message": "Order created successfully"}, status.HTTP_201_CREATED)


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
