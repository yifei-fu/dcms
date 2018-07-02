from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('user', views.UserViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url('login/', views.UserLoginView.as_view(), name='login'),
    url('logout/', views.UserLogoutView.as_view(), name='logout'),
]
