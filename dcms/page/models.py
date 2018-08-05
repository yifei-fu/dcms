from django.db import models

from content.models import ContentMetadata
from post.models import Post


class PageComponent(models.Model):
    '''
    Common elements of pages such as header, footer, etc.
    '''
    name = models.TextField()
    default_content = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Page(ContentMetadata):
    '''
    Pages returned by the CMS API consisting of ( component, content (currently posts only) ) pairs.
    '''
    name = models.TextField()
    path = models.CharField(max_length=200)
    components = models.ManyToManyField(PageComponent, through='PageLayout')
    # An optional base page is rendered before child page, which provides extra components or override existing ones.
    base_page = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class PageLayout(models.Model):
    '''
    ManyToMany relations between Page and PageComponent with extra field content.
    '''

    class Meta:
        unique_together = ('page', 'component')

    component = models.ForeignKey(PageComponent, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.ForeignKey(Post, blank=True, null=True, on_delete=models.SET_NULL)
    include_metadata = models.BooleanField(default=True)  # if the API returns metadata of the post

    def __str__(self):
        return f"{self.component} on {self.page}"
