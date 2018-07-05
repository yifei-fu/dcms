from rest_framework import serializers
from rest_framework.reverse import reverse

from content.serializers import ContentBaseSerializer
from .models import *


class AddGetComment():
    '''
    defines get_comment method for using 'comment = serializers.SerializerMethodField()' for hyperlinked serialization of comments
    '''

    def get_comment(self, obj):
        url_kwargs = {
            'content_type': ContentType.objects.get_for_model(obj).id,
            'object_id': obj.id
        }
        # self must be a subclass of Serializer
        context = getattr(self, 'context')
        request = context.get('request') if context else None
        return reverse('comment-list', kwargs=url_kwargs, request=request)


class CommentSerializer(ContentBaseSerializer):
    class Meta(ContentBaseSerializer.Meta):
        model = Comment
        fields = ('id', 'tags', 'category', 'slug', 'description', 'creation_time', 'modification_time', 'archived',
                  'content', 'author', 'replied_to')

    def validate(self, attrs):
        # add fields in context for serialization
        attrs['content_type'] = self.context['content_type']
        obj = self.context.get('obj')
        object_id = obj.id if obj else self.context['object_id']
        attrs['object_id'] = object_id

        # check replied_to
        replied_to = attrs.get('replied_to')
        if replied_to:
            if attrs.get('content_type') != replied_to.content_type or attrs.get('object_id') != replied_to.object_id:
                raise ValidationError("replied_to is either null or a comment to the same object")

        # check if object being commented has attr comment_enabled and is True
        comment_enabled = getattr(attrs.get('content_type'), 'comment_enabled', True)
        if not comment_enabled:
            raise ValidationError("comment_enabled is false on the object being commented")

        return super().validate(attrs)
