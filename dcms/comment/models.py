from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from config.settings import TEXT_PREVIEW_LEN
from content.models import ContentMetadata


class Comment(ContentMetadata):
    content = models.TextField()
    replied_to = models.ForeignKey("self", verbose_name=_("Parent comment being replied to"), on_delete=models.CASCADE,
                                   null=True, blank=True, related_name='replies')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id', )

    @property
    def content_preview(self):
        return self.content[:TEXT_PREVIEW_LEN]

    def __str__(self):
        return 'Comment "{}" by {}'.format(self.content_preview, self.author)

    # Validates that replied_to is either None or a comment to the same object.
    # attrs is either a Comment instance or data in CommentSerializer
    @classmethod
    def validate_replied_to(cls, attrs):
        replied_to = getattr(attrs, 'replied_to', None) or attrs.get('replied_to')

        if replied_to:
            content_type = getattr(attrs, 'content_type', None) or attrs.get('content_type')
            object_id = getattr(attrs, 'object_id', None) or attrs.get('object_id')
            if (replied_to.content_type != content_type or replied_to.object_id != object_id):
                raise ValidationError("replied_to is either None or a comment to the same object")

    def clean(self):
        self.validate_replied_to(self)
