from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.exceptions import ValidationError

from config.settings import TEXT_PREVIEW_LEN
from content.models import ContentMetadata


class Comment(ContentMetadata):
    content = models.TextField()
    replied_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'Comment "' + self.content[:TEXT_PREVIEW_LEN] + "'"

    def clean(self):
        # replied_to is either None or a comment to the same object
        if self.replied_to and not (self.replied_to.content_object == self.content_object):
            raise ValidationError("replied_to is either None or a comment to the same object")
