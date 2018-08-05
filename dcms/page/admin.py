from django.contrib import admin

from .models import *


class PageLayoutInline(admin.TabularInline):
    model = PageLayout
    extra = 0
    pass


class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'base_page')
    list_filter = ('base_page', 'components')
    
    inlines = (PageLayoutInline,)

admin.site.register(PageComponent)
admin.site.register(Page, PageAdmin)
