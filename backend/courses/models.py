from django.db import models

from core.constants import COURSE_TITLE_MAX_LENGTH, COURSE_DESCRIPTION_MAX_LENGTH, COURSE_AUTHOR_MAX_LENGTH


class Course(models.Model):
    author = models.CharField(
        max_length=COURSE_AUTHOR_MAX_LENGTH,
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=COURSE_TITLE_MAX_LENGTH,
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
