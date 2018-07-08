from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from config.authentication import default_authentication_classes
from generic.contenttypes_utils import ContenttypesParamsMixin
from .serializers import *


class UserVoteView(generics.RetrieveUpdateDestroyAPIView, ContenttypesParamsMixin):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = default_authentication_classes

    def get_object(self):
        try:
            return self.filter_generic_queryset(self.queryset).get(user=self.request.user)
        except models.ObjectDoesNotExist:
            return Vote(user=self.request.user, content_type=self.content_type, object_id=self.obj.id)
