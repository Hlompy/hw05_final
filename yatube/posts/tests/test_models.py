# posts/tests/tests_url.py
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='text',
        )

    def test_model_have_correct_object_names(self):
        post = self.post
        expected_post = post.text
        fields = {
            'text': expected_post
        }
        for field, expected_value in fields.items():
            with self.subTest(field=field):
                self.assertEqual(str(field), expected_value)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='title',
            slug='test-slug',
            description='Тестовое описание',
        )

    def test_models_have_correct_object_names(self):
        group = self.group
        expected_group = group.title
        fields = {
            'title': expected_group
        }
        for field, expected_value in fields.items():
            with self.subTest(field=field):
                self.assertEqual(str(field), expected_value)
