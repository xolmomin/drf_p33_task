from django.db.models import CharField, ForeignKey, CASCADE, ImageField
from django.db.models.fields import IntegerField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class Category(UUIDBaseModel):
    name = CharField(max_length=120)


class Product(CreatedBaseModel):
    name = CharField(max_length=255)
    price = IntegerField()
    image = ImageField(upload_to='products/%Y/%m/%d', validators=[])
    description = CKEditor5Field()
    category = ForeignKey('apps.Category', CASCADE)


class Order(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE)
    user = ForeignKey('apps.User', CASCADE)
    quantity = IntegerField()
