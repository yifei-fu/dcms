from rest_framework import viewsets

from content.permissions import *
from content.serializers import *
from dcms.config.authentication import default_authentication_classes
from post.models import Post
from post.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthorOrAdminOtherwiseReadOnly,)
    authentication_classes = default_authentication_classes


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = default_authentication_classes


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = default_authentication_classes
