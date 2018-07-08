from rest_framework import serializers

from content.serializers import ContentBaseSerializer
from generic.contenttypes_utils import reverse_contenttypes_url, add_contenttypes_info_from_context
from .models import *


class SerializerCommentsFieldMixin(serializers.Serializer):
    '''
    Adds fields 'comments' for hyperlinked API of comments to a given object
    '''
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        context = getattr(self, 'context')
        request = context.get('request') if context else None
        return reverse_contenttypes_url('comment-list', obj, request)


class CommentSerializer(ContentBaseSerializer):
    class Meta(ContentBaseSerializer.Meta):
        model = Comment
        fields = ('id', 'tags', 'category', 'slug', 'description', 'creation_time', 'modification_time', 'archived',
                  'content', 'author', 'replied_to')

    def validate(self, attrs):
        add_contenttypes_info_from_context(attrs, self.context)

        # check replied_to
        self.Meta.model.validate_replied_to(attrs)

        # check if object being commented has attr comment_enabled and is True
        comment_enabled = getattr(attrs.get('content_type'), 'comment_enabled', True)
        if not comment_enabled:
            raise ValidationError("comment_enabled is false on the object being commented")

        return super().validate(attrs)
