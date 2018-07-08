from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

BINARY_SCORE_OPTIONS = (-1, 1)
THREE_SCORE_OPTIONS = (1, 2, 3)
FIVE_SCORE_OPTIONS = range(1, 5 + 1)
TEN_SCORE_OPTIONS = range(1, 10 + 1)


class Vote(models.Model):
    class Meta:
        unique_together = (('user', 'content_type', 'object_id'),)

    score = models.SmallIntegerField()
    submit_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    score_options = {}

    @classmethod
    def add_score_options(cls, content_type, score_options):
        for x in score_options:
            assert (-32768 < x < 32767), "score_options values must be within the range of models.SmallIntegerField"
        cls.score_options[content_type.id] = list(score_options)

    def __str__(self):
        return 'Vote {} on {} by {}'.format(self.score, self.content_object, self.user)

    @classmethod
    def validate_score(cls, score, content_type):
        score_options = cls.score_options.get(content_type.id)
        if score_options and score not in score_options:
            raise ValidationError("Score is not in the score options defined by the model")

    def clean(self):
        self.validate_score(self.score, self.content_type)

    @classmethod
    def score_sum(cls, queryset):
        return queryset.aggregate(models.Sum('score'))['score__sum']

    @classmethod
    def avg_score(cls, queryset):
        sum = cls.score_sum(queryset)
        if not sum:
            return None
        return sum / queryset.count()

    @classmethod
    def score_distribution(cls, queryset):
        return queryset.values('score').annotate(models.Count('score'))
