from rest_framework.serializers import ModelSerializer

from apps.models import Post


class PostListModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = 'id', 'title', 'category'


class PostDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
