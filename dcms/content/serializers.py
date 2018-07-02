from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'parent', 'count')
        read_only_fields = ('count',)

    def get_count(self, obj):
        return obj.get_count(ContentMetadata.objects.all())


class TagSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('name', 'count')
        read_only_fields = ('count',)

    def get_count(self, obj):
        return obj.get_count(ContentMetadata.objects.all())
