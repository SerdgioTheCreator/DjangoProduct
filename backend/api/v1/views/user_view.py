from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.v1.serializers.user_serializer import CustomUserSerializer, PurchaseSerializer
from users.models import CustomUser, Purchase


class CustomUserViewSet(viewsets.ModelViewSet):
    """Пользователи."""

    queryset = CustomUser.objects.select_related('balance').all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)

    @action(
        methods=['patch'],
        detail=True,
        permission_classes=(IsAdminUser,),
    )
    def change_balance(self, request, pk=None):
        user = self.get_object()
        new_balance = request.data.get('balance_amount')

        user.balance.amount = new_balance
        user.balance.save()
        return Response({'detail': 'Баланс успешно изменен.'}, status=status.HTTP_200_OK)


class PurchaseViewSet(viewsets.ModelViewSet):
    """Покупки."""

    queryset = Purchase.objects.select_related('user', 'course').all()
    serializer_class = PurchaseSerializer
    http_method_names = ('get', 'head', 'options', 'delete')
    permission_classes = (IsAdminUser,)
