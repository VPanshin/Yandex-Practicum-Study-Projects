from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель Тэга."""
    name = models.CharField(
        'Тэг',
        max_length=settings.LENGTH_FOR_NAME_AND_OTHER,
        db_index=True
    )
    color = ColorField(
        'Цвет',
        max_length=settings.LENGTH_FOR_COLOR,
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=settings.LENGTH_FOR_NAME_AND_OTHER,
        unique=True,
    )

    class Meta:
        ordering = ['id', 'name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        """Метод для строкового представления в админ панели."""
        return self.name


class Recipe(models.Model):
    """Модель Рецепта."""
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг'
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient')
    )
    name = models.CharField(
        'Название рецепта',
        max_length=settings.LENGTH_FOR_NAME_AND_OTHER,
        db_index=True
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        null=True,
        blank=True
    )
    text = models.TextField(
        'Описание'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1)],
        db_index=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """Метод для строкового представления в админ панели."""
        return self.name


class Ingredient(models.Model):
    """Модель Ингредиента."""
    name = models.CharField(
        'Наименование ингридиента',
        max_length=settings.LENGTH_FOR_NAME_AND_OTHER,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.LENGTH_FOR_NAME_AND_OTHER,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Вспомогательная модель, связывающая рецепты и ингридиенты."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(1)],
        db_index=True
    )

    class Meta:
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Состав рецептов'

    def __str__(self):
        """Метод для строкового представления в админ панели."""
        return f'{self.ingredient} - {self.amount}'


class Follow(models.Model):
    """Модель Подписки."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на автора'
        constraints = [
            models.UniqueConstraint(
                name='unique_follower_user',
                fields=['user', 'following'],
            ),
        ]

    def __str__(self):
        """Метод для строкового представления в админ панели."""
        return f'{self.user} добавил в подписки {self.following}'


class ShoppingCart(models.Model):
    """Модель Списка покупок."""
    user = models.ForeignKey(
        User,
        related_name='shopping_cart',
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        """Метод для строкового представления в админ панели."""
        return f'{self.recipe}'


class Favorite(models.Model):
    """Модель Избранного."""
    user = models.ForeignKey(
        User,
        related_name='favorite_user',
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        """Метод для строкового представления в админ панели."""
        return f'У {self.user} рецепт {self.recipe} в изрбранном'
