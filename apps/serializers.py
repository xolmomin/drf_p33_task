import re
from typing import Any

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer, ListSerializer
from rest_framework_simplejwt.tokens import Token, RefreshToken

from apps.models import Product, User, Category, CartItem, Cart, Order, OrderItem


class ProductListModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'name', 'price', 'category'


class ProductRetrieveModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'name', 'price', 'category'


class CartConfirmModelSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ()


class CartItemModelSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = 'id', 'cart', 'product', 'quantity'
        read_only_fields = 'cart', 'quantity'
        # extra_kwargs = {}

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            cart = Cart.objects.create(user=user)

        return super().create(validated_data | {'cart_id': cart.id})


class CategoryListModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name'


class SendSmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')

        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs):
        phone = attrs['phone']
        user, created = User.objects.get_or_create(phone=phone)
        user.set_unusable_password()

        return super().validate(attrs)


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'phone'


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'name', 'price', 'image'


class OrderItemModelSerializer(ModelSerializer):
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = 'id', 'product', 'quantity'


class OrderModelSerializer(ModelSerializer):
    products = OrderItemModelSerializer(many=True, source='order_items', read_only=True)

    class Meta:
        model = Order
        fields = 'id', 'total_amount', 'products'


class VerifySmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    code = IntegerField(default=100100)
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs: dict[str, Any]):
        self.user = authenticate(phone=attrs['phone'], request=self.context['request'])

        if self.user is None:
            raise ValidationError(self.default_error_messages['no_active_account'])

        return attrs

    @property
    def get_data(self):
        refresh = self.get_token(self.user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        user_data = UserModelSerializer(self.user).data

        return {
            'message': "OK",
            'data': {
                **data, **{'user': user_data}
            }
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)  # type: ignore


"""
11

PageNumber                           LimitOffset

page=1 page_size=3      (3ta)        limit 3 offset 0
page=2 page_size=3      (3ta)        limit 3 offset 3
page=3 page_size=3      (3ta)        limit 3 offset 6
page=4 page_size=3      (2ta)        limit 3 offset 9




limit offset



"""