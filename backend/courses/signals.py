from django.db.models import Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.constants import GROUPS_LIMIT, ONE, USERS_LIMIT
from courses.models import Group
from users.models import Purchase


@receiver(post_save, sender=Purchase)
def post_save_group(instance, created, **kwargs):
    """
    Автоматическое равномерное распределение пользователей по
    группам после сохранения покупки курса.
    """
    if created:
        # Получаем группы с числом пользователей, сортируем по числу студентов
        groups = Group.objects.filter(course=instance.course).annotate(
            students_count=Count('users')
        ).order_by('students_count')

        # Проверяем, если все группы заполнены
        all_full = all(group.students_count >= USERS_LIMIT for group in groups)
        if len(groups) == GROUPS_LIMIT and all_full:
            raise ValueError(f"Все группы курса {instance.course} заполнены.")

        # Если групп меньше лимита, создаём новую группу
        if len(groups) < GROUPS_LIMIT:
            group = Group.objects.create(
                course=instance.course,
                title=f'Группа №{len(groups) + ONE}'
            )
        else:
            # Находим первую группу с минимальным количеством пользователей
            group = groups.first()

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
