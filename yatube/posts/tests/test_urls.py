from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus

from django.urls.base import reverse

from posts.models import Post, Group


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

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test-slug/',
            'posts/profile.html': '/profile/user/',
            'posts/post_detail.html': f'/posts/{self.post.id}/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_author_can_create(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit(self):
        response = self.authorized_author_client.get(
            f'/posts/{self.post.id}/edit'
        )
        self.assertEqual(response.status_code, HTTPStatus.MOVED_PERMANENTLY)

    def test_unexisting_page(self):
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_user_cant_enter_on_private_sites(self):
        response = self.client.get(reverse('posts:post_create'))
        response_2 = self.client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.id})
        )
        self.assertRedirects(response, '/auth/login/?next=/create/')
        self.assertRedirects(
            response_2,
            f'/auth/login/?next=/posts/{self.post.id}/edit/'
        )
