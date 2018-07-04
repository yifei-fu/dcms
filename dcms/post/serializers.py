from rest_framework import serializers

from content.models import Tag, Category
from content.serializers import ContentBaseSerializer
from .models import *


class PostSerializer(ContentBaseSerializer):
    class Meta:
        model = Post
