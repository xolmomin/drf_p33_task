from django_filters import FilterSet, NumberFilter

from apps.models import Post


class PostFilter(FilterSet):
    min_price = NumberFilter(field_name="userId", lookup_expr='gte')
    max_price = NumberFilter(field_name="userId", lookup_expr='lte')

    class Meta:
        model = Post
        fields = ('category', 'type')
