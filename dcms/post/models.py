from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
# Create your models here.
from django.utils import timezone

from comment.models import Comment
from content.models import ContentMetadata, Category


class Post(ContentMetadata):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.TextField()
    content = models.TextField()

    published = models.BooleanField(default=False)
    publish_time = models.DateTimeField()

    view_count = models.IntegerField(default=0, editable=False)

    comment_enabled = models.BooleanField()
    comment = GenericRelation(Comment)

    def __str__(self):
        return self.title

    published_query = models.Q(published=True, publish_time__lte=timezone.now())

    @classmethod
    def get_published(cls):
        return cls.objects.filter(Post.published_query)
