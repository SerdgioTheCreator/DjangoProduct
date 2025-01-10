from django.db.models.signals import post_save
from django.dispatch import receiver

from core.constants import DEFAULT_BALANCE_AMOUNT
from users.models import Balance, CustomUser


@receiver(post_save, sender=CustomUser)
def post_save_balance(sender, instance, created, **kwargs):
    """
    Автоматическое пополнение баланса пользователя
    после его сохранения.
    """

    if created:
        Balance.objects.create(user=instance, amount=DEFAULT_BALANCE_AMOUNT)
