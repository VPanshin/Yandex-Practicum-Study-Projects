import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from api_yamdb.settings import TEXT_LENGTH


User = get_user_model()


def validate_slug(value):
    reg = re.compile('^[-a-zA-Z0-9_]+$')
    if not reg.search(value):
        result = re.findall(r'[^-a-zA-Z0-9_]+', value)
        raise ValidationError(
            f'Идентификатор категории содержит недопустимый символ: {result}')


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )


class TitleCommonClass(models.Model):
    """
    Базовый (родительский) класс для Category, Genre
    """
    name = models.CharField(
        'Наименование',
        max_length=256,
        db_index=True
    )
    slug = models.CharField(
        'Идентификатор',
        max_length=50,
        unique=True,
        validators=[validate_slug]
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Category(TitleCommonClass):
    """Класс категорий."""
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(TitleCommonClass):
    """Класс жанров."""
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Класс произведений.
    Нельзя добавлять произведения, которые еще не вышли
    (год выпуска не может быть больше текущего).
    """
    name = models.CharField(
        'Наименование',
        max_length=256,
        db_index=True
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[validate_year],
        db_index=True
    )
    description = models.TextField(
        'Описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['name', '-year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class GenreTitle(models.Model):
    """Вспомогательный класс, связывающий жанры и произведения."""
    title = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genres',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_combination_gt'
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """Класс отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=True
    )
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Comment(models.Model):
    """Класс комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментрий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_LENGTH]
