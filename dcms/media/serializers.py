from rest_framework import serializers

from content.serializers import ContentBaseSerializer
from .models import *


class ImageSerializer(ContentBaseSerializer):
    class Meta(ContentBaseSerializer.Meta):
        model = Image


class FileSerializer(ContentBaseSerializer):
    class Meta(ContentBaseSerializer.Meta):
        model = File
