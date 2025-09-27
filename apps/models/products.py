from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import CharField, ForeignKey, CASCADE, ImageField, PositiveIntegerField
from django.db.models.fields import IntegerField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class Category(UUIDBaseModel):
    name = CharField(max_length=120)


class Product(CreatedBaseModel):
    name = CharField(max_length=255)
    price = IntegerField()
    description = CKEditor5Field()
    category = ForeignKey('apps.Category', CASCADE)

# class CategoryImage(CreatedBaseModel):

#     category = ForeignKey('apps.Category', CASCADE)
#     image = ImageField()
#
#
# class ProductImage(CreatedBaseModel):
#     product = ForeignKey('apps.Product', CASCADE)
#     image = ImageField()
#
# class OrderImage(CreatedBaseModel):
#     order = ForeignKey('apps.Order', CASCADE)
#     image = ImageField()
#
#
#
class Image(CreatedBaseModel):
    image = ImageField(upload_to='images/')
    content_type = ForeignKey('contenttypes.ContentType', CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
