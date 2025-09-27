from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from apps.models import Category, Order, Product, User
from apps.models.users import AdminProfile, UserProfile


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class AdminProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class UserAdminMixin(UserAdmin):
    search_fields = ['phone']
    ordering = ("phone",)
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "usable_password", "password1", "password2"),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_superuser=self.type)


class UserProfileStackedInline(admin.StackedInline):
    model = UserProfile
    min_num = 1
    extra = 1
    max_num = 1


@admin.register(UserProxy)
class UserProxyModelAdmin(UserAdminMixin):
    type = False
    list_display = ['id', 'first_name', 'last_name', 'user_address', 'user_university']
    inlines = [UserProfileStackedInline]

    # n + 1 - select_related, prefetch_related

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('userprofile')

    @admin.display(description="Address", empty_value='')
    def user_address(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.address

    @admin.display(description="University", empty_value='')
    def user_university(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.university


class AdminProfileStackedInline(admin.StackedInline):
    model = AdminProfile
    min_num = 1
    extra = 1
    max_num = 1
    readonly_fields = ['balance']


@admin.register(AdminProxy)
class AdminProxyModelAdmin(UserAdminMixin):
    type = True
    inlines = [AdminProfileStackedInline]
    list_display = ['id', 'phone', 'admin_balance']

    @admin.display(description="Balance")
    def admin_balance(self, obj):
        if hasattr(obj, 'adminprofile'):
            return obj.adminprofile.balance
        return 0


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_names']

    @admin.display(description="Product Names")
    def product_names(self, obj: Category):
        return ', '.join([product.name for product in obj.product_set.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('product_set')


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'custom_status', 'total_amount', 'product_count'

    # actions = ['make_completed']

    @admin.display(description='Status')
    def custom_status(self, obj: Order):
        if obj.status == Order.Status.IN_PROGRESS:
            emoji = '⌛️'
        elif obj.status == Order.Status.COMPLETED:
            emoji = '✅'
        else:
            emoji = '❌'
        return f"{emoji} {obj.status}"

    # @admin.action(description='Make completed')
    # def make_completed(self, request, queryset):
    #     queryset.update(status=Order.Status.COMPLETED)
    #     User.objects.filter(is_superuser=True).update(balance=F('balance') + 5000 * queryset.count())

    @admin.display(description='Product count')
    def product_count(self, obj: Order):
        return obj.order_items.count()


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'price', 'category__name'
    search_fields = 'name',

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


admin.site.unregister(Group)
