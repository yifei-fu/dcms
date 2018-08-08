from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from config.authentication import default_authentication_classes
from content.permissions import IsAuthorOrAdminOtherwiseReadOnly
from .serializers import *


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrAdminOtherwiseReadOnly)
    authentication_classes = default_authentication_classes

    def get_queryset(self):
        qs = Post.get_published(self.queryset)
        if not self.request.user.is_anonymous:
            qs = qs | Post.objects.filter(author=self.request.user.id)  # include unpublished posts from the user
        return qs
