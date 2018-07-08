from rest_framework import viewsets

from config.authentication import default_authentication_classes
from content.permissions import IsAuthorOrAdminOtherwiseReadOnly
from generic.contenttypes_utils import ContenttypesParamsMixin
from .serializers import *


class CommentViewSet(viewsets.ModelViewSet, ContenttypesParamsMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOtherwiseReadOnly,)
    authentication_classes = default_authentication_classes

    def get_queryset(self):
        return self.filter_generic_queryset(self.queryset)
