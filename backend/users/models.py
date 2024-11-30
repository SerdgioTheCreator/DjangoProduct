from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from core.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH


class User(AbstractUser):
    """Класс профиля пользователя."""

    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_STUDENT, 'Студент'),
        (ROLE_TEACHER, 'Преподаватель'),
        (ROLE_ADMIN, 'Администратор'),
    )
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text=('Обязательно для заполнения. Не более 150 символов.'
                   'Только буквы, цифры и @/./+/-/_'),
        validators=(UnicodeUsernameValidator(), ),
        error_messages={'unique': 'Это имя пользователя занято'},
        verbose_name='Уникальный юзернейм'
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        error_messages={'unique': 'Этот адрес электронной почты уже зарегистрирован'},
        blank=True,
        verbose_name='Адрес электронной почты'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='О себе'
    )
    role = models.CharField(
        max_length=max(len(role) for role, verbose in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT,
        verbose_name='Ролевая принадлежность'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id', )

    @property
    def is_teacher(self):
        return self.role == self.ROLE_TEACHER

    @property
    def is_admin(self):
        return (
                self.role == self.ROLE_ADMIN
                or self.is_superuser
                or self.is_staff
        )

    def __str__(self):
        return self.get_full_name()
