from django.test import TestCase, RequestFactory
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from .models import *
from post.models import *
from post.views import *

from utils import get_results

class ContentMetadataTestCase(TestCase):
    '''
    Testing content metadata (tags, categories) using Post model and views.
    '''

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        Category.objects.create(name='root1')
        Category.objects.create(name='root2')
        Category.objects.create(name='root1-node1', parent=Category.objects.get(name='root1'))
        Category.objects.create(name='root1-node2', parent=Category.objects.get(name='root1'))
        Category.objects.create(name='root1-node2-node1', parent=Category.objects.get(name='root1-node2'))
        self.post = Post.objects.create(title='Test Post Title', published=True,
                                        category=Category.objects.get(name='root1-node2'))
        self.post.tags.set([Tag.objects.create(name='tag1'), Tag.objects.create(name='tag2')])
        Tag.objects.create(name='tag3')

    def test_object_attrs(self):
        self.assertEqual(self.post.tags_list, 'tag1, tag2')

    def test_slug(self):
        self.assertEqual(Post.objects.first().slug, 'test-post-title')

    def test_api_get(self):
        client = APIClient()
        response = client.get(reverse('post-list') + '1/')
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data['tags']), 2)
        self.assertEqual(data['tags'][0], {'id': 1, 'name': 'tag1', 'count': 1})
        self.assertEqual(data['tags'][1], {'id': 2, 'name': 'tag2', 'count': 1})
        self.assertEqual(data['category'], 'root1-node2')

    def test_api_tag_list(self):
        client = APIClient()
        response = client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, 200)
        data = get_results(response.data)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], {'id': 1, 'name': 'tag1', 'count': 1})
        self.assertEqual(data[1], {'id': 2, 'name': 'tag2', 'count': 1})
        self.assertEqual(data[2], {'id': 3, 'name': 'tag3', 'count': 0})

    def test_api_category_list(self):
        client = APIClient()
        response = client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        data = get_results(response.data)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0], {'id': 1, 'name': 'root1', 'count': 0, 'parent': None})
        self.assertEqual(data[1], {'id': 2, 'name': 'root2', 'count': 0, 'parent': None})
        self.assertEqual(data[2], {'id': 3, 'name': 'root1-node1', 'count': 0, 'parent': 1})
        self.assertEqual(data[3], {'id': 4, 'name': 'root1-node2', 'count': 1, 'parent': 1})
        self.assertEqual(data[4], {'id': 5, 'name': 'root1-node2-node1', 'count': 0, 'parent': 4})

    def test_api_post(self):
        client = APIClient()

        client.login(username='user1', password='password')
        response = client.post(reverse('post-list'), format='json',
                               data={'title': 'New Post', 'content': 'To test adding tags and categories for contents.',
                                     'tags': ['tag2', 'new_tag'], 'category': 'root1-node2-node1'})
        self.assertEqual(response.status_code, 201)
        data = get_results(response.data)

        self.assertTrue(Tag.objects.filter(name='new_tag').exists())

        self.assertEqual(data['category'], 'root1-node2-node1')
        self.assertEqual(data['tags'][0], {'id': 2, 'name': 'tag2', 'count': 2})
        self.assertEqual(data['tags'][1], {'id': 4, 'name': 'new_tag', 'count': 1})
