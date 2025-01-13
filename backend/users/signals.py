from django.db import transaction
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


@receiver(post_save, sender=Purchase)
def post_save_purchase(instance, created, **kwargs):
    """
    Списание с баланса пользователя стоимости курса
    после сохранения его покупки.
    """

    if created:
        balance = instance.user.balance
        price = instance.course.price
        with transaction.atomic():
            if balance.amount < price:
                raise ValueError('Ошибка. Недостаточно средств для покупки курса.')
            elif not instance.course.is_active:
                raise ValueError('Ошибка. Этот курс недоступен для покупки.')
            else:
                balance.amount -= price
                balance.save()
