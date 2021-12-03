from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Post(models.Model):
    text = models.TextField(max_length=200, verbose_name="Текст")
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата",
        db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор"
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
        verbose_name="Группа",
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        'Текст'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
