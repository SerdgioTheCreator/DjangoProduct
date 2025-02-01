from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.v1.serializers.user_serializer import (CustomUserSerializer,
                                                PurchaseSerializer)
from users.models import CustomUser, Purchase


class CustomUserViewSet(viewsets.ModelViewSet):
    """Пользователи."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ('get', 'head', 'options',)
    permission_classes = (IsAdminUser,)


class PurchaseViewSet(viewsets.ModelViewSet):
    """Покупки."""

    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    http_method_names = ('get', 'head', 'options',)
    permission_classes = (IsAdminUser,)
