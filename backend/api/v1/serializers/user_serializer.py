from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Purchase


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    balance = serializers.SerializerMethodField(read_only=True)

    def get_balance(self, obj):
        return obj.balance.amount

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'balance',
            'role',
        )


class PurchaseSerializer(serializers.ModelSerializer):
    """Сериализатор покупок."""

    user = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(source='course.title', read_only=True)
    purchased_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Purchase
        fields = (
            'user',
            'course',
            'purchased_at',
        )
