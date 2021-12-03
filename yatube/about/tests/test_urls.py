from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group
from http import HTTPStatus


User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый текст',
            group=cls.group
        )

    def setUp(self):
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_author_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author_client.force_login(self.author)

    def test_about(self):
        response = self.client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech(self):
        response = self.client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
