from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.models import PublishBaseModel
from .constants import FIELD_MAX_LENGTH
from .utils import truncate_text

User = get_user_model()


class PublishedPostManager(models.Manager):
    """Кастомный менеджер для модели Post."""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True,
            )
        )


class Category(PublishBaseModel):
    """Модель категорий постов."""

    title = models.CharField(max_length=FIELD_MAX_LENGTH,
                             verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return truncate_text(self.title)


class Location(PublishBaseModel):
    """Модель местоположения."""

    name = models.CharField(max_length=FIELD_MAX_LENGTH,
                            verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return truncate_text(self.name)


class Post(PublishBaseModel):
    """Модель публикаций (постов)."""

    title = models.CharField(max_length=FIELD_MAX_LENGTH,
                             verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория'
    )

    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return truncate_text(self.title)
