from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

from comment.models import Comment
from content.models import ContentMetadata, Category
from vote.models import *


class Post(ContentMetadata):
    gen_slug_from_field = 'title'

    title = models.TextField()
    content = models.TextField()

    published = models.BooleanField(default=False)
    publish_time = models.DateTimeField(blank=True, null=True)

    view_count = models.IntegerField(default=0, editable=False)

    comment_enabled = models.BooleanField(default=True)
    comments = GenericRelation(Comment)

    votes = GenericRelation(Vote)

    def __str__(self):
        return self.title

    @classmethod
    def get_published(cls, queryset=None):
        if not queryset:
            queryset = cls.objects
        return queryset.filter(published=True, publish_time__lte=timezone.now())

    @classmethod
    def get_recent(cls, queryset=None):
        return cls.get_published(queryset).order_by('-publish_time')

    @classmethod
    def get_most_viewed(cls, queryset=None):
        return cls.get_published(queryset).order_by('-view_count')

    def save(self, *args, **kwargs):
        if self.published and not self.publish_time:
            self.publish_time = timezone.now()
        super().save(*args, **kwargs)


Vote.add_score_options(
    ContentType.objects.get_for_model(Post), TEN_SCORE_OPTIONS)
