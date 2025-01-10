from django.db import models

from core.constants import TITLE_MAX_LENGTH, COURSE_DESCRIPTION_MAX_LENGTH, COURSE_AUTHOR_MAX_LENGTH, URL_MAX_LENGTH


class Course(models.Model):
    """Модель курса."""

    author = models.CharField(
        max_length=COURSE_AUTHOR_MAX_LENGTH,
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

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Урок'
    )
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Название'
    )
    link = models.URLField(
        max_length=URL_MAX_LENGTH,
        verbose_name='Ссылка'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name='Группа'
    )
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return f'Группа {self.title} курса {self.course}'
