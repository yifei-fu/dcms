from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from config.authentication import default_authentication_classes
from content.permissions import IsAuthorOrAdminOtherwiseReadOnly
from .serializers import *


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOtherwiseReadOnly,)
    authentication_classes = default_authentication_classes

    # called before method handler, add attributes of the object being commented on from URL parameters
    def initial(self, request, *args, **kwargs):
        self.content_type = get_object_or_404(ContentType, id=self.kwargs['content_type'])
        self.obj = get_object_or_404(self.content_type.model_class(), id=self.kwargs['object_id'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(content_type=self.kwargs['content_type'], object_id=self.kwargs['object_id'])

    def get_serializer_context(self):
        return {'content_type': self.content_type, 'obj': self.obj, 'object_id': self.obj.id}
