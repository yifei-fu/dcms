from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from post import apiviews

router = DefaultRouter()
router.register(r'article', apiviews.ArticleViewSet)
router.register(r'tag', apiviews.TagViewSet)
router.register(r'category', apiviews.CategoryViewSet)
urlpatterns = [
    url(r'', include(router.urls)),
]
