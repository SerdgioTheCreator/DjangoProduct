from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.constants import GROUPS_LIMIT, ONE, USERS_LIMIT
from courses.models import Group
from users.models import Purchase


@receiver(post_save, sender=Purchase)
def post_save_group(instance, created, **kwargs):
    """
    Автоматическое распределение пользователей по
    группам после сохранения покупки курса.
    """
    if created:
        groups = Group.objects.filter(course=instance.course).prefetch_related('users')
        last_group = groups.last()

        # Если групп у курса нет
        if not groups.exists():
            group = Group.objects.create(course=instance.course, title='Группа №1')

        # Если групп меньше лимита групп и последняя группа заполнена
        elif len(groups) < GROUPS_LIMIT and last_group.users.count() == USERS_LIMIT:
            group = Group.objects.create(course=instance.course, title=f'Группа №{len(groups) + ONE}')

        # Если групп меньше или равно лимиту групп и последняя группа не заполнена
        elif len(groups) <= GROUPS_LIMIT and last_group.users.count() < USERS_LIMIT:
            group = last_group

        else:
            raise ValueError(f'Ошибка. Все группы курса {instance.course} заполнены.')

        group.users.add(instance.user)


@receiver(post_delete, sender=Purchase)
def post_delete_group(instance, using, **kwargs):
    """
    Удаление пользователя из группы курса после удаления его покупки.

    Если после удаления группа становится пустой, она также удаляется.
    """
    group = Group.objects.select_related(
        'course'
    ).prefetch_related(
        'users'
    ).get(
        course=instance.course, users=instance.user
    )

    group.users.remove(instance.user)

    if not group.users.exists():
        group.delete()
