from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tag', views.TagViewSet)
router.register(r'category', views.CategoryViewSet)
urlpatterns = [
    url(r'', include(router.urls)),
]
