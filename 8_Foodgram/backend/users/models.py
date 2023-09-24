from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель Пользователя."""
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin')
    ]

    email = models.EmailField(
        'Почта',
        max_length=settings.LENGTH_FOR_EMAIL,
        unique=True
    )
    username = models.SlugField(
        'Логин',
        max_length=settings.LENGTH_FOR_USER,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Поле не должно содержать символы:'
                '!#$%%^&*()=,<>?/\\|{}[]:; \n')
        ]
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.LENGTH_FOR_USER,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LENGTH_FOR_USER,
    )
    role = models.CharField(
        max_length=settings.LENGTH_FOR_ROLE,
        choices=ROLES,
        default=USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        """Метод для строкового представления в админ панели."""
        return self.username
