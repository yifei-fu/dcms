from rest_framework import serializers

from generic.contenttypes_utils import reverse_contenttypes_url, add_contenttypes_info_from_context
from .models import *


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    score_options = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = ('id', 'score', 'submit_time', 'user', 'score_options')
        read_only_fields = ('id', 'submit_time', 'content_type', 'object_id')

    def get_score_options(self, obj):
        return Vote.score_options.get(obj.content_type.id)

    def validate(self, attrs):
        add_contenttypes_info_from_context(attrs, self.context)

        self.Meta.model.validate_score(attrs['score'], attrs['content_type'])
        return super().validate(attrs)


class SerializerVotesFieldMixin(serializers.Serializer):
    '''
    Adds fields 'votes' for hyperlinked API of comments to a given object
    '''
    user_vote = serializers.SerializerMethodField()
    votes_score_avg = serializers.SerializerMethodField()
    votes_count = serializers.SerializerMethodField()
    votes_score_distribution = serializers.SerializerMethodField()

    def get_user_vote(self, obj):
        context = getattr(self, 'context')
        request = context.get('request') if context else None
        return reverse_contenttypes_url('user_vote', obj, request)

    def get_votes_score_avg(self, obj):
        return Vote.avg_score(obj.votes.all())

    def get_votes_count(self, obj):
        return obj.votes.count()

    def get_votes_score_distribution(self, obj):
        return Vote.score_distribution(obj.votes)
