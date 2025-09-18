from django.contrib.auth.models import AbstractUser
from django.db.models import CharField

from apps.models.base import UUIDBaseModel


def phone_validator(value):
    print(value)
    return value


class User(AbstractUser, UUIDBaseModel):
    phone = CharField(max_length=15, unique=True, validators=[phone_validator])
    email = None
    username = None
    password = None

    USERNAME_FIELD = 'phone'

