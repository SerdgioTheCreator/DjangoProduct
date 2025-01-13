from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Balance, CustomUser, Purchase


@receiver(post_save, sender=CustomUser)
def post_save_balance(instance, created, **kwargs):
    """
    Автоматическое пополнение баланса пользователя
    после сохранения его создания.
    """

    if created:
        Balance.objects.create(user=instance)
