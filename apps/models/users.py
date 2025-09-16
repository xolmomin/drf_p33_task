from django.contrib.auth.models import AbstractUser

from apps.models.base import UUIDBaseModel


class User(AbstractUser, UUIDBaseModel):
    pass
