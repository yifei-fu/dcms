from rest_framework import serializers

from content.serializers import ContentBaseSerializer
from post.serializers import PostSerializer
from .models import *


class PageSerializer(ContentBaseSerializer):
    components = serializers.StringRelatedField(many=True)
    contents = serializers.SerializerMethodField()

    class Meta(ContentBaseSerializer.Meta):
        model = Page

    @classmethod
    def get_page_posts_dict(cls, page):
        '''
        :return: a dict of posts, key is component id and value is (post_id, include_metadata)
        '''
        if not page:
            return {}

        # posts from base page
        posts_dict = {}
        if page.base_page:
            posts_dict = cls.get_page_posts_dict(page.base_page)

        # posts from this page
        for x in PageLayout.objects.filter(page=page):
            posts_dict[x.component] = (x.content or x.component.default_content, x.include_metadata)

        return posts_dict

    def get_contents(self, obj):
        posts_dict = self.get_page_posts_dict(obj)
        ret = []
        for component, (post, include_metadata) in posts_dict.items():
            if include_metadata:
                ret.append({'name': component.name, **PostSerializer(post).data})
            else:
                # no metadata, content only
                ret.append({'name': component.name, 'content': post.content})
        return ret
