from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models, transaction

from core.constants import DEFAULT_BALANCE_AMOUNT, EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from courses.models import Course


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_STUDENT, 'Студент'),
        (ROLE_TEACHER, 'Преподаватель'),
        (ROLE_ADMIN, 'Администратор'),
    )
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text=('Обязательно для заполнения. Не более 150 символов.'
                   'Только буквы, цифры и @/./+/-/_'),
        validators=(UnicodeUsernameValidator(), ),
        error_messages={'unique': 'Это имя пользователя занято'},
        verbose_name='Уникальный юзернейм'
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        error_messages={'unique': 'Этот адрес электронной почты уже зарегистрирован'},
        blank=True,
        verbose_name='Адрес электронной почты'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='О себе'
    )
    role = models.CharField(
        max_length=max(len(role) for role, verbose in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT,
        verbose_name='Ролевая принадлежность'
    )
    groups = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()

    @property
    def is_teacher(self):
        return self.role == self.ROLE_TEACHER

    @property
    def is_admin(self):
        return (
                self.role == self.ROLE_ADMIN
                or self.is_superuser
                or self.is_staff
        )

    def has_access_to_course(self, course):
        return Purchase.objects.filter(user=self, course=course).exists()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id', )


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name='Пользователь'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество бонусов',
        default=DEFAULT_BALANCE_AMOUNT
    )

    def __str__(self):
        return f'Баланс пользователя {self.user.get_full_name()}: {self.amount}'

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class PurchaseManager(models.Manager):
    @staticmethod
    def create_purchase(user, course):
        """Метод покупки курса пользователем."""

        with transaction.atomic():
            if not course.is_active:
                raise ValueError('Этот курс недоступен для покупки.')

            if user.balance.amount < course.price:
                raise ValueError('Недостаточно средств для покупки курса.')

            user.balance.amount -= course.price
            user.balance.save()

            purchase = Purchase.objects.create(user=user, course=course)
            return purchase


class Purchase(models.Model):
    """Модель покупки курса пользователем."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='buyer',
        verbose_name='Покупатель'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course',
        verbose_name='Курс'
    )
    purchased_at = models.DateTimeField(
        verbose_name='Дата покупки',
        auto_now_add=True
    )

    objects = PurchaseManager()

    def __str__(self):
        return f'Пользователь {self.user.get_full_name()} приобрел курс - {self.course}'

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course')
        ]
