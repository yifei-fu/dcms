from rest_framework import serializers
from comment.serializers import AddGetComment
from content.models import Tag, Category
from content.serializers import ContentBaseSerializer
from .models import *
from comment.views import *


class PostSerializer(ContentBaseSerializer, AddGetComment):
    comment = serializers.SerializerMethodField()

    class Meta(ContentBaseSerializer.Meta):
        model = Post
        read_only_fields = ContentBaseSerializer.Meta.read_only_fields + ('comment',)
