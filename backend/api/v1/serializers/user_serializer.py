from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from users.models import Purchase


class CustomUserSerializer(UserCreateSerializer):
    """Пользователи."""

    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'

    ROLE_CHOICES = (
        (ROLE_STUDENT, 'Студент'),
        (ROLE_TEACHER, 'Преподаватель'),
    )

    balance_amount = serializers.IntegerField(source='balance.amount', read_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, label='Ролевая принадлежность', default=ROLE_STUDENT)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, label='Пароль')

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'balance_amount',
            'role',
            'password',
        )


class PurchaseSerializer(serializers.ModelSerializer):
    """Покупки."""

    user = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    purchased_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Purchase
        fields = (
            'user',
            'course',
            'purchased_at',
        )
