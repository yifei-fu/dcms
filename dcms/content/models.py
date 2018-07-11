from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_count(self, queryset):
        return queryset.filter(category_pk=self.pk).count()


class Tag(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    # get or create tags from text of comma-separated tags
    @classmethod
    def tag_objects(cls, tags):
        if not tags:
            return []
        if type(tags) is str:
            tags = tags.split(',')
        tags = [tag.strip() for tag in tags]  # remove extra blank char
        tags = {slugify(tag) for tag in filter(lambda tag: len(tag) != 0, tags)}  # remove empty, duplicate and slugify
        return [cls.objects.get_or_create(name=tag)[0] for tag in tags]

    def get_count(self, queryset):
        return queryset.filter(tags__in=[self.id]).count()


# abstract base class for all media contents, stores metadata
class ContentMetadata(models.Model):
    class Meta:
        abstract = True

    gen_slug_from_field = 'name'  # field provided by subclasses to generate slug

    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    creation_time = models.DateTimeField(_('creation date'), blank=True, null=True, auto_now_add=True)
    modification_time = models.DateTimeField(_('modification date'), blank=True, null=True, auto_now=True)
    author = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)

    archived = models.BooleanField(default=False)

    @property
    def tags_list(self):
        return ", ".join([tag for (tag,) in self.tags.values_list('name')])

    @classmethod
    def active_objects(cls):
        return cls.objects.filter(archived=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_source = getattr(self, self.gen_slug_from_field, None)
            if slug_source:
                self.slug = slugify(slug_source)
        super().save(*args, **kwargs)
