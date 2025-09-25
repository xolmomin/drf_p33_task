import asyncio
import threading
import time

from django.contrib.auth import get_user_model
from django.db.models import ForeignKey, CASCADE, OneToOneField, TextChoices, CharField, F
from django.db.models.fields import IntegerField

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class Cart(UUIDBaseModel):
    user = OneToOneField('apps.User', CASCADE)


class CartItem(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='cart_items')
    cart = ForeignKey('apps.Cart', CASCADE, related_name='cart_items')
    quantity = IntegerField(db_default=1)


class Order(CreatedBaseModel):
    class Status(TextChoices):
        IN_PROGRESS = "in_progress", 'In Progress'
        CANCELLED = "cancelled", 'Cancelled'
        COMPLETED = "completed", 'Completed'

    status = CharField(max_length=15, choices=Status.choices, default=Status.IN_PROGRESS)
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    total_amount = IntegerField()

    def superuser_add_balance(self):
        print("superuser_add_balance")
        if self.status == Order.Status.COMPLETED:
            User = get_user_model()
            User.objects.filter(is_superuser=True).update(balance=F('balance') + 5000)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        threading.Thread(target=self.superuser_add_balance).start()
        # self.superuser_add_balance()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class OrderItem(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='order_items')
    order = ForeignKey('apps.Order', CASCADE, related_name='order_items')
    quantity = IntegerField(db_default=1)
    price = IntegerField()
