from django.apps import apps
from rest_framework import serializers

from config.settings import TAG_COUNT_MODELS, CATEGORY_COUNT_MODELS
from .models import *


class TagsField(serializers.Field):
    '''
    comma-separated tags
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        return [TagSerializer(x).data for x in obj.all()]

    def to_internal_value(self, data):
        return Tag.tag_objects(data)

class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'parent', 'count')
        read_only_fields = ('count',)

    def get_count(self, obj):
        count = 0
        for app_label, model_name in TAG_COUNT_MODELS:
            count += obj.get_count(apps.get_model(app_label, model_name).objects.all())
        return count


class TagSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('count',)

    def get_count(self, obj):
        count = 0
        for app_label, model_name in CATEGORY_COUNT_MODELS:
            count += obj.get_count(apps.get_model(app_label, model_name).objects.all())
        return count
