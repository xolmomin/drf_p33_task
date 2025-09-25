from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import F

from apps.models import Category, Order, Product, User


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'custom_status', 'total_amount', 'product_count'
    actions = ['make_completed']

    @admin.display(description='Status')
    def custom_status(self, obj: Order):
        if obj.status == Order.Status.IN_PROGRESS:
            emoji = '⌛️'
        elif obj.status == Order.Status.COMPLETED:
            emoji = '✅'
        else:
            emoji = '❌'
        return f"{emoji} {obj.status}"

    @admin.action(description='Make completed')
    def make_completed(self, request, queryset):
        queryset.update(status=Order.Status.COMPLETED)
        User.objects.filter(is_superuser=True).update(balance=F('balance') + 5000 * queryset.count())

    @admin.display(description='Product count')
    def product_count(self, obj: Order):
        return obj.order_items.count()


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'price'
    search_fields = 'name',


admin.site.unregister(Group)
