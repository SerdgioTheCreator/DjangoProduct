from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Balance, CustomUser


@receiver(post_save, sender=CustomUser)
def post_save_custom_user(instance, created, **kwargs):
    """
    Автоматическое создание баланса пользователя
    после сохранения создания объекта пользователя.
    """

    if created:
        Balance.objects.create(user=instance)
