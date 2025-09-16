from django.contrib import admin
from django.contrib.auth.models import Group

from apps.models import Category, Order, Product


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
