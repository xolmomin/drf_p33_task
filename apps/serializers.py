from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.models import Product, User


class RegisterModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    username = CharField(default="botir")

    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        username = attrs.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")

        if password != confirm_password:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class ProductListModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'name', 'price', 'category'
