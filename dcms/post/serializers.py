from comment.views import *
from vote.serializers import SerializerVotesFieldMixin
from .models import *


class PostSerializer(ContentBaseSerializer,
                     SerializerCommentsFieldMixin,
                     SerializerVotesFieldMixin):

    class Meta(ContentBaseSerializer.Meta):
        model = Post
        read_only_fields = ContentBaseSerializer.Meta.read_only_fields + ('comment', 'author')

    def create(self, validated_data):
        if not validated_data.get('author'):
            validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('hide_content'):
            data.pop('content')
        return data
