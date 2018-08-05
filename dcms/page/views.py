from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from config.authentication import default_authentication_classes
from content.permissions import IsAuthorOrAdminOtherwiseReadOnly
from .serializers import *


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrAdminOtherwiseReadOnly)
    authentication_classes = default_authentication_classes
