from rest_framework.serializers import ModelSerializer

from apps.models import Product


class ProductListModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'name', 'price', 'category'
