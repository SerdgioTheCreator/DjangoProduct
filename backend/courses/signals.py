from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import Group
from users.models import Purchase


@receiver(post_save, sender=Purchase)
def post_save_group(sender, instance, created, **kwargs):
    """
    Автоматическое распределение пользователей по
    группам после сохранения покупки курса.
    """

    if created:
        user = instance.user
        course = instance.course
        group = Group.objects.filter(
            course=course
        ).annotate(
            students_count=Count('users')
        ).order_by(
            'students_count'
        ).first()

        if group:
            user.group = group
            user.save()

        #  добавить:
        #  создание группы, если групп у курса еще нет
        #  удаление пользователя из группы при потере доступа к курсу (post_delete)
        #  избегать N + 1 (select_related, prefetch_related)
