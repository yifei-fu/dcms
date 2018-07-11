from django.contrib import admin

from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'tags_list', 'content_preview', 'replied_to_id',
                    'creation_time', 'modification_time')
    list_display_links = ('id', 'content_preview',)
    list_filter = ('category', 'creation_time', 'modification_time', 'author')
    search_fields = ('id', 'author', 'category', 'tags_list', 'content')
    date_hierarchy = 'creation_time'

    filter_horizontal = ('tags',)


admin.site.register(Comment, CommentAdmin)
