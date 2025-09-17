from django.http import HttpResponse
from rest_framework import generics
from .serializers import CategorySerializer, PostSerializer, PostDetailSerializer

from .models import Category, Post


def index(request):
    return HttpResponse("==Blog Index==")


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None  # disables pagination here


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
