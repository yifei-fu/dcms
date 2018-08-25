from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

import re

from config.authentication import default_authentication_classes
from content.permissions import IsAuthorOrAdminOtherwiseReadOnly
from .serializers import *


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrAdminOtherwiseReadOnly)
    authentication_classes = default_authentication_classes

    ALLOWED_FILTER_PARAMS = {
        'category': 'category__name',
        'tags': 'tags__in',
        'creation_time_lte': 'creation_time__lte',
        'creation_time_gte': 'creation_time__gte',
        'modification_time_lte': 'modification_time__lte',
        'modification_time_gte': 'modification_time__gte',
        'author_id': 'author__id',
        'author': 'author__username',
        'archived': 'archived',
        'title': 'title',
        'title_contains': 'title__contains',
        'content_contains': 'content__contains',
        'publish_time_lte': 'publish_time__lte',
        'publish_time_gte': 'publish_time__gte',
        'view_count_lte': 'view_count__lte',
        'view_count_gte': 'view_count__gte',
        'comment_enabled': 'comment_enabled',
    }

    def filter_objects(self, qs, query_params=None):
        if not query_params:
            query_params = self.request.query_params
        filter_kwargs = {}
        for field, value in query_params.items():
            if not field in self.ALLOWED_FILTER_PARAMS:
                raise ParseError(code=400, detail="Invalid filter argument")
            filter_kwargs[self.ALLOWED_FILTER_PARAMS[field]] = value
        return qs.filter(**filter_kwargs).distinct()

    def get_queryset(self):
        qs = Post.get_published(self.queryset)
        if not self.request.user.is_anonymous:
            qs = qs | Post.objects.filter(author=self.request.user.id)  # include unpublished posts from the user

        # filtering using query params
        qs = self.filter_objects(qs)

        return qs

    def list(self, request, *args, **kwargs):
        self.get_serializer_context = lambda: {'hide_content': True}
        data = super().list(request, *args, **kwargs)
        return data
