from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models

from core.constants import (
    COURSE_AUTHOR_MAX_LENGTH,
    COURSE_DESCRIPTION_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    URL_MAX_LENGTH,
)


class Course(models.Model):
    """Модель курса."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        max_length=COURSE_AUTHOR_MAX_LENGTH,
        related_name='courses',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        null=True,
        max_length=COURSE_DESCRIPTION_MAX_LENGTH,
        verbose_name='Описание'
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоимость'
    )
    is_active = models.BooleanField(
        verbose_name='Доступность'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Проверка, что создатель курса является преподавателем или администратором."""
        if not (self.author.is_teacher or self.author.is_admin):
            raise PermissionDenied('Создавать курсы могут только преподаватели или администраторы.')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)


class Lesson(models.Model):
    """Модель урока."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Название'
    )
    link = models.URLField(
        max_length=URL_MAX_LENGTH,
        verbose_name='Ссылка'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)


class Group(models.Model):
    """Модель группы."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name='Курс'
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='groups',
        verbose_name='Участники'
        )
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Название'
    )

    def __str__(self):
        return f'Группа {self.title} курса {self.course}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('id',)
