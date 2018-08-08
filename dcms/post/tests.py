from django.test import TestCase, RequestFactory
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from post.admin import PostAdmin
from .models import *
from .views import *


class PostTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username='user1', password='password',
                                              is_staff=True, is_superuser=True)
        self.user2 = User.objects.create_user(username='user2', password='password',
                                              is_staff=True, is_superuser=False)
        self.time_now = timezone.now()
        self.posts = [Post.objects.create(title="Post #1", content="Post #1 content",
                                          author=self.user1, published=True,
                                          publish_time=self.time_now + timezone.timedelta(days=-1)),
                      Post.objects.create(title="Post #2", content="Post #2 content",
                                          author=self.user1, published=True, view_count=10),
                      Post.objects.create(title="Post #3", content="Post #3 content",
                                          author=self.user2, published=True,
                                          publish_time=self.time_now + timezone.timedelta(days=1)),
                      Post.objects.create(title="Post #4", content="Post #4 content",
                                          author=self.user2, published=False, view_count=20)
                      ]
        self.list_url = reverse('post-list')

    def test_objects(self):
        self.assertEqual(len(self.posts), Post.objects.count())

    def test_classmethods(self):
        self.assertEqual(set(Post.get_published()), {self.posts[0], self.posts[1]})
        self.assertEqual(list(Post.get_recent().values_list('id', flat=True)),
                         [2, 1])
        self.assertEqual(list(Post.get_most_viewed().values_list('id', flat=True)),
                         [2, 1])

    # API tests

    # test post list
    def test_posts_list_anonymous_user(self):
        client = APIClient()
        response = client.get(self.list_url)
        self.assertIs(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[1]['id'], 2)

        self.assertEqual(data[0]['title'], "Post #1")
        self.assertEqual(data[0]['content'], "Post #1 content")
        self.assertEqual(data[0]['published'], True)
        self.assertIsNotNone(data[1]['publish_time'])

    # test if list API returns the unpublished post when the request user is user2
    def test_posts_list_user_unpublished(self):
        client = APIClient()
        client.login(username='user2', password='password')
        response = client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data), 4)
        self.assertEqual(data[3]['id'], 4)
        self.assertEqual(data[3]['published'], False)

    def test_post_create(self):
        client = APIClient()

        # must be authenticated to create a new post
        response = client.post(self.list_url, data={'title': "New Post through API", 'content': "New post content"})
        self.assertEqual(response.status_code, 403)

        client.login(username='user1', password='password')
        response = client.post(self.list_url, data={'title': "New Post through API", 'content': "New post content",
                                                    'tags': []})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Post.objects.last().id, 5)
        self.assertEqual(Post.objects.last().title, "New Post through API")
        self.assertEqual(Post.objects.last().content, "New post content")
