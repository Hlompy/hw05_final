from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

from ..forms import PostForm

from ..models import Follow, Group, Post, Comment

User = get_user_model()


class Views(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.author = User.objects.create_user(username='author')
        cls.follower = User.objects.create_user(username='follower')
        cls.form = PostForm()
        cls.group = Group.objects.create(
            title='Заголовок',
            slug='test-slug',
            description='Текст',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group,
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            text='Testing comment',
            post=cls.post,
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
        self.guest_client = Client()
        self.follower_client = Client()
        self.authorized_client = Client()
        self.authorized_author_client = Client()
        self.authorized_client.force_login(self.user)
        self.follower_client.force_login(self.follower)
        self.authorized_author_client.force_login(self.author)

    def test_urls_uses_correct_template(self):
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}):
            'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
            'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
            'posts/post_create.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_post(self, post):
        author = self.author.username
        text = self.post.text
        post_id = self.post.id
        group = self.group.title
        self.assertEqual(author, 'author')
        self.assertEqual(text, 'Тестовый текст')
        self.assertEqual(post_id, 1)
        self.assertEqual(group, 'Заголовок')

    def test_home_page_show_correct_context(self):
        response = self.guest_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        self.check_post(first_object)

    def test_group_list_correct_context(self):
        group = Views.group
        group_list = reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}
        )
        response = self.guest_client.get(group_list)
        first_object = response.context['page_obj'][0]
        self.check_post(first_object)
        self.assertEqual(first_object.group.slug, group.slug)

    def test_profile_correct_context(self):
        profile = reverse(
            'posts:profile',
            kwargs={'username': self.user.username}
        )
        response = self.authorized_client.get(profile)
        first_object = response.context['username']
        self.check_post(first_object)
        self.assertEqual(first_object, self.user)
        self.assertTrue(
            first_object,
            Post.objects.filter(author=self.user)
        )

    def test_post_detail_correct_context(self):
        post_detail = reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}
        )
        response = self.authorized_client.get(post_detail)
        first_object = response.context['post_id']
        self.check_post(first_object)
        self.assertEqual(first_object, self.post.id)
        self.assertTrue(first_object,
                        Post.objects.filter(id=self.post.id))

    def test_post_edit(self):
        post_edit = reverse(
            'posts:post_edit',
            kwargs={'post_id': self.post.id}
        )
        response = self.authorized_client.get(post_edit)
        first_object = response.context['post']
        self.check_post(first_object)
        self.assertTrue(first_object.id,
                        Post.objects.filter(id=self.post.id))

    def test_post_create(self):
        post_create = reverse('posts:post_create')
        post_edit = reverse(
            'posts:post_edit', kwargs={'post_id': self.post.id}
        )
        response = self.authorized_client.get(post_create)
        response_2 = self.authorized_client.get(post_edit)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.ModelChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(response_2.context['is_edit'], True)

    def test_cache(self):
        post_count = Post.objects.count()
        content = self.client.get(reverse('posts:index')).content
        Post.objects.filter(id=1).delete()
        content_after_delete = self.client.get(reverse('posts:index')).content
        post_2 = Post.objects.count()
        self.assertEqual(content, content_after_delete)
        self.assertNotEqual(post_count, post_2)

    def test_comments_on_post_detail_page(self):
        comment_text = 'Testing comment'
        comments = Comment.objects.create(
            author=self.user,
            text=comment_text,
            post=self.post,
        )
        post_detail = reverse('posts:post_detail',
                              kwargs={'post_id': self.post.id})
        response = self.authorized_client.get(
            post_detail)
        comment = response.context['post'].comments.all()[0]
        self.assertTrue(
            comment, Comment.objects.filter(author=comments.author)
        )

    def test_follow(self):
        Follow.objects.create(user=self.follower, author=self.user)
        following = reverse(
            'posts:profile_follow',
            kwargs={'username': self.user.username}
        )
        profile = reverse(
            'posts:profile',
            kwargs={
                'username': self.user.username
            }
        )
        response = self.follower_client.post(
            following,
            follow=True
        )
        self.assertRedirects(response, profile)
        self.assertTrue(
            Follow.objects.filter(
                user=self.follower,
                author=self.user).exists()
        )

    def test_unfollow(self):
        Follow.objects.create(user=self.follower, author=self.user)
        unfollow = reverse(
            'posts:profile_unfollow', kwargs={'username': self.user.username}
        )
        profile = reverse(
            'posts:profile',
            kwargs={'username': self.user.username}
        )
        response = self.follower_client.post(
            unfollow,
            follow=True
        )
        self.assertRedirects(response, profile)
        self.assertFalse(
            Follow.objects.filter(
                user=self.follower,
                author=self.user).exists()
        )
