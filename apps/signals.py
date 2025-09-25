import time

from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.models import Order, User


# @receiver(post_save, sender=Order)
# def my_handler(sender, **kwargs):
#     time.sleep(5)
#     if kwargs['instance'].status == Order.Status.COMPLETED:
#         User.objects.filter(is_superuser=True).update(balance=F('balance') + 5000)
