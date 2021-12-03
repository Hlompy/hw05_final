from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Group, Post, User

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Заголовок',
            slug='test-slug',
            description='Текст'
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

    def setUp(self):
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_author_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author_client.force_login(self.author)

    def test_authorized_client_create_page(self):
        post_count = Post.objects.count()
        posts = Post.objects.all()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
            'image': self.uploaded
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': self.user.username}
        ))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            form_data,
            Post.objects.filter(
                text='Тестовый текст',
                group=self.group.id,
                image=self.uploaded
            ).exists()
        )
        self.assertEqual(
            form_data['image'].open().read(), posts[0].image.read()
        )
        self.assertEqual(
            form_data['image'].open().read(), posts[0].image.read()
        )

    def test_guest_client_can_create_new_post(self):
        form_data = {
            'text': 'Текст поста гостя',
            'group': self.group.id,
            'image': self.uploaded
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        login = reverse('login')
        new = reverse('posts:post_create')
        redirect = login + '?next=' + new
        self.assertRedirects(response, redirect)
        self.assertFalse(
            Post.objects.filter(
                text=form_data['text'],
                group=self.group,
                image=self.uploaded).exists())

    def test_post_edit_form(self):
        post = Post.objects.create(
            text='Текст поста',
            author=self.author,
            group=self.group
        )
        form_data = {
            'text': 'Текст поста редактирования',
            'group': self.group,
            'author': self.author
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': post.id}
        ))
        post.refresh_from_db()
        self.assertNotEqual(post.text, form_data['text'])
        self.assertEqual(post.group, form_data['group'])
        self.assertEqual(post.author, form_data['author'])
