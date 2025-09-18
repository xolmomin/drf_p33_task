from typing import Optional, Any

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.tokens import Token

from apps.models import Product, User
from apps.utils import send_sms_code, random_code


class ProductListModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'name', 'price', 'category'


class CustomAccessTokenSerializer(Serializer):
    username_field = User.USERNAME_FIELD
    CharField()
    token_class: Optional[type[Token]] = None

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = CharField(write_only=True, default='901001010')

    def send_code(self):
        code = random_code()
        send_sms_code(self.user.phone, code)

    def validate(self, attrs: dict[str, Any]):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field]
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            raise ValidationError(self.default_error_messages['no_active_account'])

        self.send_code()
        return {
            'message': "sms code sent",
            'data': None
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)  # type: ignore
