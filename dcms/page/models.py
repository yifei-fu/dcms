from django.db import models

from content.models import ContentMetadata
from post.models import Post


class PageComponent(models.Model):
    name = models.TextField()
    default_content = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Page(ContentMetadata):
    name = models.TextField()
    url = models.TextField()
    components = models.ManyToManyField(PageComponent, through='PageLayout')

    def __str__(self):
        return self.name


class PageLayout(models.Model):
    component = models.ForeignKey(PageComponent, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
