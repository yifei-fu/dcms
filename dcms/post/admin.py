from django.contrib import admin

from .models import *


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)


make_published.short_description = "Publish selected posts"


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'tags_list', 'title', 'published', 'publish_time')
    list_display_links = ('id', 'title',)
    list_filter = ('category', 'published', 'publish_time', 'creation_time', 'modification_time', 'author')
    search_fields = ('id', 'author', 'category', 'tags_list', 'title')
    date_hierarchy = 'publish_time'

    actions = (make_published,)

    filter_horizontal = ('tags',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs.filter(author=request.user)
        return qs


admin.site.register(Post, PostAdmin)
