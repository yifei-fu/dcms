from rest_framework import viewsets

from content.permissions import *
from content.serializers import *
from config.authentication import default_authentication_classes
from post.models import Post


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = default_authentication_classes


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = default_authentication_classes
