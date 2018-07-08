from comment.views import *
from vote.serializers import SerializerVotesFieldMixin
from .models import *


class PostSerializer(ContentBaseSerializer,
                     SerializerCommentsFieldMixin,
                     SerializerVotesFieldMixin):

    class Meta(ContentBaseSerializer.Meta):
        model = Post
        read_only_fields = ContentBaseSerializer.Meta.read_only_fields + ('comment',)
