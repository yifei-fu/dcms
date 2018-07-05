from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'(?P<content_type>\d+)/(?P<object_id>\d+)', CommentViewSet)
urlpatterns = [
    url(r'', include(router.urls)),
]
