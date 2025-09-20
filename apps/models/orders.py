from django.db.models import ForeignKey, CASCADE, OneToOneField
from django.db.models.fields import IntegerField

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class Cart(UUIDBaseModel):
    user = OneToOneField('apps.User', CASCADE)


class CartItem(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='cart_items')
    cart = ForeignKey('apps.Cart', CASCADE, related_name='cart_items')
    quantity = IntegerField(db_default=1)


class Order(UUIDBaseModel):
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    total_amount = IntegerField()


class OrderItem(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='order_items')
    order = ForeignKey('apps.Order', CASCADE, related_name='order_items')
    quantity = IntegerField(db_default=1)
    price = IntegerField()
