from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.filters import PostFilter
from apps.models import Post
from apps.serializers import PostDetailModelSerializer, PostListModelSerializer


class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    # filterset_fields = ('category', 'type')
    filterset_class = PostFilter
    search_fields = ('title',)


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailModelSerializer



"""
posts, comments
api list (6)


filter(posts - user_id, comments-post_id)
search(posts - title, comments-email,name)


GET	/posts/1/comments
GET	/comments?postId=1




"""