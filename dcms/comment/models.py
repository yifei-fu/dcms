from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from config.settings import TEXT_PREVIEW_LEN
from content.models import ContentMetadata


class Comment(ContentMetadata):
    content = models.TextField()
    replied_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, editable=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'Comment "' + self.content[:TEXT_PREVIEW_LEN] + "'"
