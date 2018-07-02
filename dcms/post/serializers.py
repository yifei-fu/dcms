from rest_framework import serializers

from content.models import Tag, Category
from .models import *


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', allow_null=True, queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'creation_time', 'modification_time', 'view_count')
