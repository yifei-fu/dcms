from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_count(self, queryset):
        return queryset.filter(category_pk=self.pk).count()


class Tag(models.Model):
    name = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    # get or create tags from text of comma-separated tags
    @classmethod
    def tag_objects(cls, text):
        if not text:
            return []
        tags = [tag.strip() for tag in text.split(',')]  # remove extra blank char
        tags = {slugify(tag) for tag in filter(lambda tag: len(tag) != 0, tags)}  # remove empty, duplicate and slugify
        return [cls.objects.get_or_create(name=tag) for tag in tags]

    def get_count(self, queryset):
        return queryset.filter(tags__contains=self).count()


# abstract base class for all media contents, stores metadata
class ContentMetadata(models.Model):
    class Meta:
        abstract = True

    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    creation_time = models.DateTimeField(_('creation date'), blank=True, null=True, auto_now_add=True)
    modification_time = models.DateTimeField(_('modification date'), blank=True, null=True, auto_now=True)
    author = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)

    archived = models.BooleanField(default=True)

    def __str__(self):
        return f"Content Object {self.slug}"

    @classmethod
    def active_objects(cls):
        return cls.objects.filter(archived=False)
