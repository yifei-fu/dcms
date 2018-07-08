from django.conf.urls import url

from generic.contenttypes_utils import *
from .views import *

urlpatterns = [
    url(r'user_vote/' + CONTENTTYPES_PARAMS_URL, UserVoteView.as_view(), name='user_vote'),
]
