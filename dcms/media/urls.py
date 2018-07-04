from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('image', ImageViewSet)
router.register('file', FileViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^upload_image/(?P<filename>[^/]+)$', ImageUploadView.as_view()),
    url(r'^upload_file/(?P<filename>[^/]+)$', FileUploadView.as_view()),
]
