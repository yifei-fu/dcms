from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from generic.contenttypes_utils import *
from .views import *

router = DefaultRouter()
router.register(CONTENTTYPES_PARAMS_URL, CommentViewSet)
urlpatterns = [
    url(r'', include(router.urls)),
]
